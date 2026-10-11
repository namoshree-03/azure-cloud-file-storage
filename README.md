# ☁️ Cloud-Based File Storage & Sharing System

A web-based cloud file storage application that allows users to **upload, view, download, and delete files** through a simple and user-friendly interface.

The application is built using **Python Flask** and uses **Microsoft Azure Blob Storage** for cloud-based file storage. The Flask web application is deployed on **Microsoft Azure App Service**, making it accessible through the internet.

## 🌐 Live Demo

🔗 **[Open the Live Application on Microsoft Azure](https://namoshree-cloud-files-2026-hvcdape0dwcwawc8.indiasouthcentral-01.azurewebsites.net/)**

**Hosting Platform:** Microsoft Azure App Service  
**Cloud Storage:** Microsoft Azure Blob Storage

## 📌 Project Overview

The Cloud-Based File Storage & Sharing System provides a simple solution for managing files using cloud storage. Users can upload files through the web application, store them in Microsoft Azure Blob Storage, view the available files, download files when required, and delete files.

The project demonstrates how a Python web application can integrate with a cloud storage service using the Azure Storage Blob SDK and be deployed on a cloud platform.

## ✨ Features

- 📤 Upload files to cloud storage
- 📁 View uploaded files
- ⬇️ Download stored files
- 🗑️ Delete files
- ☁️ Store files using Microsoft Azure Blob Storage
- 🌐 Access the application through a public URL
- 📱 Simple and user-friendly interface
- 🔗 Integration of Flask with Azure Blob Storage

## 🏗️ System Architecture

```text
                 User / Browser
                       |
                       v
              +-------------------+
              |   Azure App       |
              |   Service         |
              |   Flask App       |
              +---------+---------+
                        |
                        | Azure Storage Blob SDK
                        v
              +-------------------+
              | Microsoft Azure   |
              | Blob Storage       |
              +---------+---------+
                        |
                        v
                 uploads Container
```

GitHub Actions is used to automate the configured build and deployment workflow for Azure App Service.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML | Frontend structure |
| CSS | User interface styling |
| Microsoft Azure Blob Storage | Cloud file storage |
| Azure Storage Blob SDK | Integration with Azure Blob Storage |
| Microsoft Azure App Service | Web application hosting |
| GitHub Actions | Automated build and deployment |
| GitHub | Source code management |
| Gunicorn | Production web server |

## 📂 Project Structure

```text
azure-cloud-file-storage/
│
├── main.py
├── requirements.txt
├── README.md
│
└── templates/
    └── index.html
```

## ⚙️ How the System Works

1. The user opens the deployed web application in a browser.
2. The user selects a file to upload.
3. The Flask application receives and processes the file.
4. Flask connects to Microsoft Azure Blob Storage using the Azure Storage SDK.
5. The file is uploaded to the configured `uploads` container.
6. The application retrieves and displays the stored files.
7. Users can download or delete files through the web interface.

## ☁️ Cloud Implementation

### 1. Microsoft Azure App Service

Azure App Service is used to host the Flask web application. It provides a public URL through which users can access the application over the internet.

**Live URL:**

https://namoshree-cloud-files-2026-hvcdape0dwcwawc8.indiasouthcentral-01.azurewebsites.net/

### 2. Microsoft Azure Blob Storage

Azure Blob Storage is used to store uploaded files in the cloud.

The application uses the Azure Storage Blob SDK to communicate with the storage service.

**Container name:** `uploads`

### 3. GitHub Actions

GitHub Actions runs the configured build and deployment workflow. The workflow integrates with Azure App Service to deploy the application.

### 4. GitHub

GitHub is used to maintain the project's source code, track changes, and support the deployment workflow.

## 🔐 Security

- Azure Storage credentials should be configured using environment variables or Azure App Service application settings.
- Connection strings, access keys, and other secrets should never be committed to the GitHub repository.
- Uploaded files should be validated and filenames handled securely.
- Storage access permissions should be configured according to the application's requirements.

## 🚀 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/namoshree-03/azure-cloud-file-storage.git
cd azure-cloud-file-storage
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Configure the following variables with your own values:

```text
AZURE_STORAGE_CONNECTION_STRING=<your-azure-storage-connection-string>
CONTAINER_NAME=uploads
SECRET_KEY=<your-secret-key>
```

Set these variables in your local environment before running the application. Do not publish actual credentials.

### 4. Run the Application

```bash
python main.py
```

Open the local URL displayed by Flask in your browser. If the application is configured to use port 8080, the URL will be:

```text
http://127.0.0.1:8080
```

## 🎯 Objective

To develop and deploy a cloud-based file management system that enables users to upload, view, download, and delete files through a web interface while using Microsoft Azure Blob Storage for cloud-based file storage.

## 📚 Cloud Computing Concepts Demonstrated

- Cloud Storage
- Cloud Application Deployment
- Storage as a Service
- Cloud Service Integration
- Remote File Access
- Cloud Storage APIs and SDKs
- Environment-Based Configuration
- Automated Deployment using GitHub Actions

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

🌐 **Live Application — Microsoft Azure:**  
https://namoshree-cloud-files-2026-hvcdape0dwcwawc8.indiasouthcentral-01.azurewebsites.net/

💻 **GitHub Repository:**  
https://github.com/namoshree-03/azure-cloud-file-storage

👩‍💻 **GitHub Profile:**  
https://github.com/namoshree-03
