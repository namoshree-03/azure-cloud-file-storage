import os
import sqlite3
from io import BytesIO
from functools import wraps
from pathlib import Path

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, send_file, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")

if os.environ.get("WEBSITE_INSTANCE_ID") and not secret_key:
    raise RuntimeError("SECRET_KEY must be configured in Azure.")

app.secret_key = secret_key or "local-development-only-change-me"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(
        bool(os.environ.get("WEBSITE_INSTANCE_ID"))
        or os.environ.get("FLASK_ENV") == "production"
    ),
)


AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("CONTAINER_NAME", "uploads")

# App Service's /home directory is persistent when App Service storage is enabled.
if os.environ.get("WEBSITE_INSTANCE_ID"):
    DATA_DIR = Path("/home/data")
else:
    DATA_DIR = Path(app.instance_path)
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE = DATA_DIR / "users.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()


init_db()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def get_container_client():
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise RuntimeError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable is not set."
        )
    service = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )
    return service.get_container_client(CONTAINER_NAME)


def user_blob_name(filename):
    # Every account gets its own virtual folder/prefix in the private container.
    return f"user_{session['user_id']}/{filename}"


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    container_client = get_container_client()
    prefix = f"user_{session['user_id']}/"
    files = []

    for blob in container_client.list_blobs(name_starts_with=prefix):
        display_name = blob.name[len(prefix):]
        if not display_name:
            continue
        size_kb = (blob.size or 0) / 1024
        created = (
            blob.creation_time.strftime("%d-%m-%Y %H:%M")
            if blob.creation_time else "-"
        )
        files.append({
            "name": display_name,
            "size": f"{size_kb:.1f} KB",
            "created": created
        })

    files.sort(key=lambda item: item["created"], reverse=True)
    return render_template("index.html", files=files, email=session.get("email"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not email or "@" not in email:
            flash("Enter a valid email address.", "error")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
        elif password != confirm_password:
            flash("Passwords do not match.", "error")
        else:
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (email, generate_password_hash(password))
                )
                db.commit()
                flash("Account created. Please log in.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("An account with that email already exists.", "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT id, email, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            return redirect(url_for("index"))

    return render_template("login.html")


@app.post("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.post("/upload")
@login_required
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file or not uploaded_file.filename:
        flash("Please select a file.", "error")
        return redirect(url_for("index"))

    filename = secure_filename(uploaded_file.filename)
    if not filename:
        flash("Invalid file name.", "error")
        return redirect(url_for("index"))

    try:
        blob_client = get_container_client().get_blob_client(user_blob_name(filename))
        blob_client.upload_blob(uploaded_file.stream, overwrite=True)
        flash(f"'{filename}' uploaded successfully to Azure Blob Storage.", "success")
    except Exception:
        app.logger.exception("File upload failed")
        flash("Upload failed. Check the Azure Storage configuration and application logs.", "error")

    return redirect(url_for("index"))


@app.get("/download/<path:filename>")
@login_required
def download(filename):
    safe_name = secure_filename(os.path.basename(filename))
    if not safe_name or safe_name != filename:
        flash("Invalid file name.", "error")
        return redirect(url_for("index"))

    try:
        blob_client = get_container_client().get_blob_client(user_blob_name(safe_name))
        data = blob_client.download_blob().readall()
        properties = blob_client.get_blob_properties()
        content_type = (
            properties.content_settings.content_type or "application/octet-stream"
        )
        return send_file(
            BytesIO(data),
            as_attachment=True,
            download_name=safe_name,
            mimetype=content_type
        )
    except Exception:
        app.logger.exception("File download failed")
        flash("File not found or could not be downloaded.", "error")
        return redirect(url_for("index"))


@app.post("/delete/<path:filename>")
@login_required
def delete(filename):
    safe_name = secure_filename(os.path.basename(filename))
    if not safe_name or safe_name != filename:
        flash("Invalid file name.", "error")
        return redirect(url_for("index"))

    try:
        get_container_client().get_blob_client(user_blob_name(safe_name)).delete_blob()
        flash(f"'{safe_name}' deleted from Azure Blob Storage.", "success")
    except Exception:
        app.logger.exception("File deletion failed")
        flash("File not found or could not be deleted.", "error")

    return redirect(url_for("index"))


@app.get("/health")
def health():
    return {"status": "ok", "service": "Azure Cloud File Storage System"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
