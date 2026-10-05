# ☁️ Cloud-Based File Storage & Sharing System

A web-based cloud file storage application that allows users to **upload, view, download, and delete files** through a simple and user-friendly interface.

The application is built using **Python Flask** and uses **Microsoft Azure Blob Storage** for cloud-based file storage. The Flask web application is deployed on **Render**, making it accessible through the internet.

## 🌐 Live Demo

🔗 **[Open the Live Application](https://namoshree-cloud-files-2026.onrender.com)**

## 📌 Project Overview

The Cloud-Based File Storage & Sharing System provides a simple solution for managing files using cloud storage. Users can upload files through the web application, store them in Microsoft Azure Blob Storage, view the available files, download files when required, and delete files.

The project demonstrates how a web application can integrate with a cloud storage service using the Azure Blob Storage SDK.

## ✨ Features

- 📤 Upload files to cloud storage
- 📁 View uploaded files
- ⬇️ Download files
- 🗑️ Delete files
- ☁️ Store files using Microsoft Azure Blob Storage
- 🌐 Access files through a web application
- 📱 Responsive and user-friendly interface
- 🔗 Flask integration with Azure Blob Storage

## 🏗️ System Architecture

```text
                 User / Browser
                       │
                       ▼
              ┌─────────────────┐
              │     Render      │
              │   Flask App     │
              └────────┬────────┘
                       │
                       │ Azure Blob SDK
                       ▼
              ┌─────────────────┐
              │ Microsoft Azure │
              │  Blob Storage   │
              └────────┬────────┘
                       │
                       ▼
                  uploads
                   Container
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML | Frontend structure |
| CSS | User interface |
| Microsoft Azure Blob Storage | Cloud file storage |
| Azure Storage Blob SDK | Azure integration |
| Render | Application hosting |
| GitHub | Source code management |
| Gunicorn | Production web server |

## 📂 Project Structure

```text
azure-cloud-file-storage/
│
├── main.py
├── requirements.txt
│
└── templates/
    └── index.html
```

## ⚙️ How the System Works

1. The user opens the web application.
2. The user selects a file to upload.
3. The Flask application receives the file.
4. Flask connects to Microsoft Azure Blob Storage using the Azure Storage SDK.
5. The file is uploaded to the `uploads` container.
6. Stored files are retrieved and displayed on the website.
7. Users can download or delete files through the application.

## ☁️ Cloud Implementation

### Microsoft Azure Blob Storage

Azure Blob Storage is used as the primary cloud storage service.

The application stores uploaded files inside the:

```text
uploads
```

Blob container.

### Render

The Flask web application is hosted on Render and is accessible through the internet.

### GitHub

GitHub is used for source code management and continuous deployment.

## 🔐 Security

- Azure Storage credentials are stored using environment variables.
- Sensitive connection strings are **not stored in the GitHub repository**.
- The Azure Blob container is configured as private.
- Uploaded filenames are processed using secure filename handling.
- Secret keys are stored as environment variables.

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/namoshree-03/azure-cloud-file-storage.git
cd azure-cloud-file-storage
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Set the following variables:

```text
AZURE_STORAGE_CONNECTION_STRING=<your-azure-storage-connection-string>
CONTAINER_NAME=uploads
SECRET_KEY=<your-secret-key>
```

> ⚠️ Never upload your Azure connection string, access keys, or other credentials to GitHub.

### 4. Run the application

```bash
python main.py
```

The application will be available at:

```text
http://127.0.0.1:8080
```

## 🎯 Objective

To develop a cloud-based file management system that enables users to upload, view, download, and delete files while storing them securely using Microsoft Azure Blob Storage.

## 📚 Cloud Computing Concepts Demonstrated

- Cloud Storage
- Cloud Application Deployment
- Storage as a Service
- Cloud Service Integration
- Remote File Access
- Cloud Storage APIs and SDKs
- Environment-Based Configuration

## 🌟 Future Enhancements

- User authentication and authorization
- File sharing through generated links
- File search and filtering
- File size and type restrictions
- Folder-based organization
- Cloud-based user management
- File preview functionality

## 👩‍💻 Author

**Namoshree Badkhal**

BE Computer Engineering  
AISSMS College of Engineering, Pune

## 🔗 Project Links

🌐 **Live Application:**  
https://namoshree-cloud-files-2026.onrender.com

💻 **GitHub Repository:**  
https://github.com/namoshree-03/azure-cloud-file-storage
