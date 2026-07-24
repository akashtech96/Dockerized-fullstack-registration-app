# Docker Assignment - Architecture Documentation

## Overview

This project is a Dockerized Full Stack Application consisting of two independent services:

- Frontend (Express.js)
- Backend (Flask)
- Cloud Database (MongoDB Atlas)

Docker Compose is used to build, run, and connect both containers through a private Docker network.

---

# System Architecture

```
                +----------------------+
                |      User Browser    |
                | http://localhost:3000|
                +----------+-----------+
                           |
                           |
                           ▼
                +----------------------+
                | Frontend Container   |
                |      Express.js      |
                |      Port: 3000      |
                +----------+-----------+
                           |
          HTTP Request     |
     http://backend:5000
                           |
                           ▼
                +----------------------+
                | Backend Container    |
                |        Flask         |
                |      Port: 5000      |
                +----------+-----------+
                           |
                           |
                           ▼
                +----------------------+
                |   MongoDB Atlas      |
                | Cloud NoSQL Database |
                +----------------------+
```

---

# Components

## 1. Frontend

Technology:
- Node.js
- Express.js

Responsibilities:

- Display Registration Form
- Accept user input
- Send data to Flask Backend
- Display success message

Docker Container:

frontend

Port:

3000

---

## 2. Backend

Technology:

- Python
- Flask

Responsibilities:

- Receive POST request
- Validate form data
- Connect to MongoDB Atlas
- Insert records
- Return response to frontend

Docker Container:

backend

Port:

5000

---

## 3. Database

Technology:

MongoDB Atlas

Responsibilities:

- Store Registration Data
- Store Timestamp
- Cloud-hosted NoSQL database

Collection:

flask-tutorial

Database:

Test

---

# Docker Compose

Docker Compose is responsible for:

- Building frontend image
- Building backend image
- Starting both containers
- Creating Docker Network
- Connecting frontend and backend

Command:

```bash
docker compose up --build
```

---

# Container Networking

Docker Compose automatically creates an internal network.

Instead of using:

```
localhost:5000
```

the frontend communicates using the service name:

```
http://backend:5000
```

Docker automatically resolves the service name "backend" to the backend container.

---

# Environment Variables

Sensitive information is stored inside:

```
backend/.env
```

Example:

```env
MONGO_URI=your_mongodb_connection_string
```

Advantages:

- Keeps credentials outside source code
- Improves security
- Easier deployment
- Environment-specific configuration

The `.env` file is excluded from GitHub using:

```
.gitignore
```

---

# Docker Images

Two Docker Images are created.

1.

Frontend Image

```
docker_assignment-frontend
```

2.

Backend Image

```
docker_assignment-backend
```

Both images are published to Docker Hub.

---

# Docker Hub

Published Images

- docker-assignment-frontend
- docker-assignment-backend

---

# Project Workflow

1. User opens application in browser.
2. Express frontend displays registration form.
3. User submits details.
4. Frontend sends POST request to Flask backend.
5. Flask processes request.
6. Flask inserts data into MongoDB Atlas.
7. Backend returns success response.
8. Frontend displays confirmation.

---

# Technologies Used

- Docker
- Docker Compose
- Python
- Flask
- Node.js
- Express.js
- MongoDB Atlas
- Git
- GitHub
- Docker Hub

---

# Skills Demonstrated

This project demonstrates practical knowledge of:

- Docker Image Creation
- Docker Compose
- Multi-container Architecture
- Flask API Development
- Express.js Development
- MongoDB Atlas Integration
- Environment Variables
- Container Networking
- Git Version Control
- GitHub Repository Management
- Docker Hub Image Publishing

Docker_Assignment/
│
├── README.md               ← Project overview
├── docs/
│     ├── architecture.md   ← System design
│     ├── setup.md          ← Installation guide
│     └── troubleshooting.md← Problems faced and solutions