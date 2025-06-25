# Secure File Sharing System (FastAPI)

A secure file-sharing REST API built using **FastAPI** that allows two types of users **Ops** and **Client** to interact with files securely. This includes file uploads (restricted to certain types), email verification, login, and secure downloads using encrypted links.

---

## Features

### Ops User

- Login
- Upload files (`.pptx`, `.docx`, `.xlsx` only)

### Client User

- Sign Up (returns an encrypted verification URL)
- Email verification
- Login
- List uploaded files
- Download files via secure encrypted link

---

## Tech Stack

- **FastAPI** - Web framework
- **SQLite** - Lightweight database (can be swapped with PostgreSQL/MySQL)
- **Passlib + Bcrypt** - Password hashing
- **Python’s `cryptography`** - For encrypted download URLs
- **Pytest + HTTPX** - Unit testing

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/khushipy/secure-file-sharing-api.git
cd secure-file-sharing-api
```

2. **Create virtual environment and activate**

```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Start the FastAPI server**

```bash
uvicorn app.main:app --reload
```

5. **Visit Docs**

```
http://127.0.0.1:8000/docs
```

---

## Upload & Download Flow

- Ops user uploads a file via `/upload` (only if authenticated).
- Client user signs up and gets a simulated email with verification link.
- Once verified and logged in, client can:
  - List files via `/files`
  - Request download via `/download-file/{file_id}` → returns encrypted download URL.
  - Download via `/access-file/{encrypted_url}`

---

##  Unit Tests

We use **`pytest`** with **`httpx.AsyncClient`** to simulate endpoints.

### Run tests:

```bash
pytest tests/
```

 Includes test coverage for:

- Auth (sign up, login)
- Upload (ops-only)
- Download (client-only with encrypted URL)

---

## Snapshots

**SignUp**
![Screenshot 2025-06-25 135732](https://github.com/user-attachments/assets/9f38f373-4097-4d36-add5-4eee3d51b5fb)

**Email-verification**
![email-verification-ez](https://github.com/user-attachments/assets/44957399-89d2-4f54-9dc1-2c9bd9f87078)

**Login**
![Screenshot 2025-06-25 140437](https://github.com/user-attachments/assets/57ea6ddb-f325-4c39-abf8-928417229a86)

**Client Users can't Upload**
![client-can't-upload](https://github.com/user-attachments/assets/3a655669-e9aa-4a0f-b544-1b1d6106231a)

**Successfully Uploaded File**
![file-upload-ez](https://github.com/user-attachments/assets/d7d1eefd-3865-46f1-b39a-679e47d3d781)

**Download-link Generated**
![download-link-ez](https://github.com/user-attachments/assets/18d39a77-1ab0-49de-baf5-2360b76fbe64)

**File Downloaded** 
![download-ez](https://github.com/user-attachments/assets/23119187-4873-482c-83c3-5b92f659188e)

**File-list**
![get-file-ez](https://github.com/user-attachments/assets/820445ba-47b7-415f-86dc-262d710c7781)




##  Deployment Plan

Though this is a local system, here's how you can deploy it in production:

1. Use **Gunicorn** + **Uvicorn workers**
2. Set up **PostgreSQL** or another production-grade DB
3. Serve with **Nginx** as reverse proxy
4. Add **HTTPS (Let's Encrypt)** for secure transfer
5. Use **Docker** or services like **Render/Heroku** for containerized deployment
6. Enable **logging, monitoring**, and **environment variables**

---

## Security Highlights

- Passwords are hashed with bcrypt
- Emails must be verified before login
- Download links are encrypted and access-controlled
- Only specific file types are allowed for upload

---

## Author

Khushi Pal  
[GitHub](https://github.com/khushipy)

---

> Made with 💙 using FastAPI
