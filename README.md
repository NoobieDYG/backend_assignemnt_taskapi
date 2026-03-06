# 🗂️ Task Management API (Backend Assignemt for Primetrade.ai )

A production-style **Task Management REST API** built with **FastAPI**, **PostgreSQL**, and **JWT authentication**. Designed to demonstrate backend engineering best practices including dependency injection, role-based authorization, secure authentication, and database session management.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Authentication Flow](#-authentication-flow)
- [Role-Based Authorization](#-role-based-authorization)
- [Database Configuration](#-database-configuration)
- [Environment Variables](#-environment-variables)
- [Local Setup](#-local-setup)
- [Swagger API Docs](#-swagger-api-docs)
- [Testing with Postman](#-testing-with-postman)
- [Docker Setup](#-docker-setup)
- [Error Handling](#-error-handling)
- [API Versioning](#-api-versioning)
- [Future Improvements](#-future-improvements)
- [Key Concepts Demonstrated](#-key-concepts-demonstrated)

---

## ✨ Features

- 🔐 User authentication via **JWT tokens**
- 👥 **Role-based authorization** — `Admin` and `User` roles
- ✅ Full **Task CRUD** operations
- 🔒 Secure **password hashing** with bcrypt
- 🌍 **Environment variable** configuration via `.env`
- 🗄️ **Database session management** with SQLAlchemy
- ⚠️ Proper **HTTP error handling**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Hashing | bcrypt (passlib) |
| Environment Config | python-dotenv |
| API Testing | Postman |
| Package Management | Poetry / pip |
| Deployment | Docker |

---

## 📁 Project Structure

```
project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schema.py
│   ├── auth.py
│   ├── authentication.py
│   ├── auth_router.py
│   ├── task_router.py
│   └── frontend/
│       ├── index.html
│       ├── dashboard.html
│       ├── register.html
│       ├── script.js
│       └── styles.css
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## 🔐 Authentication Flow

Users authenticate via a **JWT token** using the following workflow:

```
Client ──► POST /auth/login
              │
              ▼
       Verify credentials
              │
              ▼
       Generate JWT token
              │
              ▼
       Return token to client

Client ──► Protected endpoint
       Authorization: Bearer <JWT_TOKEN>
              │
              ▼
       Token verified by middleware
              │
              ▼
       Request allowed if valid
```

**Example request header:**

```http
Authorization: Bearer <JWT_TOKEN>
```

**Login endpoint:**

```http
POST /api/v1/auth/login
```

**Request body:**

```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

**Response:**

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

The `OAuth2PasswordBearer` scheme automatically extracts the token from the `Authorization` header, validates it, and passes user info to the route:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
```

### JWT Expiration

When a token is created, an expiration timestamp is embedded in its payload:

```python
expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
```

During verification, the JWT library automatically checks whether the token has expired:

```python
jwt.decode(token, SECRET_KEY)
# Raises an exception if current_time > exp
```

---

## 👥 Role-Based Authorization

Two roles are supported:

| Role | Access Level |
|---|---|
| `user` | Standard task operations |
| `admin` | Full access including privileged endpoints |

Restrict routes to admins using the `get_admin_user` dependency:

```python
user = Depends(get_admin_user)
```

**Example — Admin-only delete endpoint:**

```python
@router.delete("/delete/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_admin_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}
```

---

## 🗄️ Database Configuration

Database connection is managed in `database.py`:

```python
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass
```

### Why `SessionLocal`?

SQLAlchemy interacts with the database through a **Session**, which is responsible for:

- Executing queries
- Tracking objects
- Committing changes
- Rolling back transactions

```python
session.add(task)
session.commit()
session.refresh(task)
```

### `get_db` Dependency

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This dependency:
1. Creates a new database session per request
2. Provides it to the route handler
3. Automatically closes it when the request finishes

```python
db: Session = Depends(get_db)
```

### Why `Base` Exists

```python
class Base(DeclarativeBase):
    pass
```

`Base` is the parent class for all database models, allowing SQLAlchemy to register models, create tables automatically, and map Python objects to database tables:

```python
class User(Base):
    __tablename__ = "users"
```

---

## 🌍 Environment Variables

Sensitive configuration is stored in a `.env` file and **must never be committed to version control**.

**`.env` example:**

```env
DATABASE_URL=postgresql://username:password@localhost:5432/tasksdb
SECRET_KEY=supersecretkey
```

**Loading variables in code:**

```python
from dotenv import load_dotenv
load_dotenv()
```

**`.gitignore` — always include:**

```gitignore
.env
__pycache__
*.pyc
```

---

## 🚀 Local Setup

Follow these steps to run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/backend_assignemnt_taskapi.git
cd backend_assignemnt_taskapi
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
poetry install
```

### 4. Create the Environment File

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/tasksdb
SECRET_KEY=supersecretkey
```

> ⚠️ Replace `postgres`, `password`, and `tasksdb` with your actual PostgreSQL credentials.

### 5. Set Up the PostgreSQL Database

Make sure PostgreSQL is running, then create the database:

```bash
createdb tasksdb
```

Or via `psql`:

```sql
CREATE DATABASE tasksdb;
```

### 6. Run Database Migrations

SQLAlchemy will auto-create tables on startup, or you can run:

```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 7. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be running at:

```
http://127.0.0.1:8000
```

---

## 📖 Swagger API Docs

FastAPI automatically generates **interactive API documentation** — no extra setup required.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

The Swagger UI allows you to:
- Browse all available endpoints
- View request/response schemas
- Authenticate using your JWT token directly in the browser
- Execute live API calls

**To authenticate in Swagger UI:**
1. Click the **Authorize 🔒** button (top right)
2. Enter: `Bearer <your_JWT_token>`
3. Click **Authorize** — all subsequent requests will include your token

### ReDoc (Alternative Docs)

```
http://127.0.0.1:8000/redoc
```

ReDoc provides a clean, read-only reference view of the full API schema — useful for sharing with external stakeholders.

### OpenAPI Schema (Raw JSON)

```
http://127.0.0.1:8000/openapi.json
```

---

## 🧪 Testing with Postman

### Step 1 — Login and Get Token

**Endpoint:** `POST /api/v1/auth/login`

**Body (JSON):**

```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 2 — Use the Token

In Postman, add the following header to all protected requests:

```
Authorization: Bearer <JWT_TOKEN>
```

Or use Postman's **Authorization tab** → select `Bearer Token` → paste the token.

---

## 🐳 Docker Setup

### Dockerfile

```dockerfile
FROM python:3.14-slim

WORKDIR /app


RUN pip install poetry


COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi


COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build the Image

```bash
docker build -t task-api .
```

### Run the Container

```bash
docker run -p 8000:8000 task-api
```

### Pass Environment Variables

```bash
docker run --env-file .env -p 8000:8000 task-api
```

> The API will be accessible at `http://localhost:8000`

---

## ⚠️ Error Handling

FastAPI uses `HTTPException` for structured API error responses.

```python
if not task:
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

**Common HTTP error codes:**

| Code | Meaning |
|---|---|
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Resource Not Found |
| `500` | Internal Server Error |

---

## 🔢 API Versioning

The API uses URL-based versioning to ensure backward compatibility as the API evolves:

```
/api/v1/tasks
/api/v2/tasks
```

Versioning prevents breaking older clients when endpoints change or are deprecated.

---

## 🔮 Future Improvements

- [ ] Redis caching for performance
- [ ] Rate limiting per user/IP
- [ ] Refresh token support
- [ ] OAuth providers (Google / GitHub login)
- [ ] Celery background task processing
- [ ] API logging and monitoring (e.g. Sentry, Datadog)
- [ ] Cursor-based pagination for task lists
- [ ] Unit and integration tests with `pytest`
- [ ] CI/CD pipeline with GitHub Actions

---

## 🧠 Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| REST API Design | FastAPI router-based structure |
| Authentication | JWT with `OAuth2PasswordBearer` |
| Authorization | Role-based dependency injection |
| Dependency Injection | `Depends()` for DB sessions and auth |
| ORM | SQLAlchemy models and sessions |
| Password Security | bcrypt hashing via `passlib` |
| Configuration | `.env` via `python-dotenv` |
| Error Handling | `HTTPException` with status codes |
| Project Structure | Modular, production-style layout |
| Containerization | Docker with environment variable support |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).