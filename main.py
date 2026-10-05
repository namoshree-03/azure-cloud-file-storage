
import os
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

from azure.storage.blob import BlobServiceClient


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "cloud-project-demo-key"
)


# ---------------------------------------------------------
# Azure Blob Storage Configuration
# ---------------------------------------------------------

AZURE_STORAGE_CONNECTION_STRING = os.environ.get(
    "AZURE_STORAGE_CONNECTION_STRING"
)

CONTAINER_NAME = os.environ.get(
    "CONTAINER_NAME",
    "uploads"
)


def get_container_client():
    """
    Creates and returns an Azure Blob Storage container client.
    """

    if not AZURE_STORAGE_CONNECTION_STRING:
        raise RuntimeError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable is not set."
        )

    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )

    return blob_service_client.get_container_client(
        CONTAINER_NAME
    )


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.route("/")
def index():

    container_client = get_container_client()

    files = []

    blobs = container_client.list_blobs()

    for blob in blobs:

        size_kb = (
            blob.size / 1024
            if blob.size
            else 0
        )

        created = (
            blob.creation_time.strftime("%d-%m-%Y %H:%M")
            if blob.creation_time
            else "-"
        )

        files.append(
            {
                "name": blob.name,
                "size": f"{size_kb:.1f} KB",
                "created": created
            }
        )

    # Show newest files first
    files.sort(
        key=lambda x: x["created"],
        reverse=True
    )

    return render_template(
        "index.html",
        files=files
    )


# ---------------------------------------------------------
# Upload File
# ---------------------------------------------------------

@app.post("/upload")
def upload():

    uploaded_file = request.files.get("file")

    if not uploaded_file or not uploaded_file.filename:

        flash(
            "Please select a file.",
            "error"
        )

        return redirect(
            url_for("index")
        )


    filename = secure_filename(
        uploaded_file.filename
    )


    if not filename:

        flash(
            "Invalid file name.",
            "error"
        )

        return redirect(
            url_for("index")
        )


    container_client = get_container_client()

    blob_client = container_client.get_blob_client(
        filename
    )


    try:

        blob_client.upload_blob(
            uploaded_file.stream,
            overwrite=True
        )

        flash(
            f"'{filename}' uploaded successfully to Azure Blob Storage.",
            "success"
        )

    except Exception as e:

        flash(
            f"Upload failed: {str(e)}",
            "error"
        )


    return redirect(
        url_for("index")
    )


# ---------------------------------------------------------
# Download File
# ---------------------------------------------------------

@app.get("/download/<path:filename>")
def download(filename):

    container_client = get_container_client()

    blob_client = container_client.get_blob_client(
        filename
    )


    try:

        download_stream = blob_client.download_blob()

        data = download_stream.readall()

        properties = blob_client.get_blob_properties()

        content_type = (
            properties.content_settings.content_type
            or "application/octet-stream"
        )


        return send_file(

            BytesIO(data),

            as_attachment=True,

            download_name=os.path.basename(
                filename
            ),

            mimetype=content_type
        )


    except Exception:

        flash(
            "File not found.",
            "error"
        )

        return redirect(
            url_for("index")
        )


# ---------------------------------------------------------
# Delete File
# ---------------------------------------------------------

@app.post("/delete/<path:filename>")
def delete(filename):

    container_client = get_container_client()

    blob_client = container_client.get_blob_client(
        filename
    )


    try:

        blob_client.delete_blob()

        flash(
            f"'{filename}' deleted from Azure Blob Storage.",
            "success"
        )

    except Exception:

        flash(
            "File not found.",
            "error"
        )


    return redirect(
        url_for("index")
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "Azure Cloud File Storage System"
    }


# ---------------------------------------------------------
# Run Application
# ---------------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            8080
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )