# 📅 Real-Time Appointment Booking System

A high-performance, asynchronous REST API built with **FastAPI** and **PostgreSQL**. This system demonstrates advanced Python concepts including Object-Oriented Programming (OOP), custom decorators, asynchronous programming, and real-time communication via WebSockets.

## 🚀 Features

* **User Management**: Role-based access (Client/Provider) with profile management.
* **Appointment CRUD**: Full lifecycle management (Create, Read, Update, Cancel) with date-based filtering.
* **Real-time Updates**: Instant broadcasting of booking changes to all connected clients using WebSockets.
* **API Security**: Protected endpoints using API Key-based authentication.
* **Advanced Python Patterns**:
* **Async/Await**: Non-blocking database and network operations.
* **Custom Decorators**: Execution timing and logging.
* **Generators**: Efficient database session management.
* **OOP**: Inheritance-based user models and encapsulated logic.



---

## 🛠️ Technical Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL (via `asyncpg` & `SQLAlchemy`)
* **Real-time**: WebSockets
* **Testing**: Pytest & HTTPX
* **Environment**: Python 3.13+

---

## 📥 Installation & Setup

### 1. Prerequisites

Ensure you have **PostgreSQL** installed and running. Create a database named `appointment_db`.

### 2. Clone and Prepare Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi[all] sqlalchemy[asyncio] asyncpg pytest httpx

```

### 3. Database Configuration

Update the `DATABASE_URL` in `app/database.py` with your PostgreSQL credentials:

```python
DATABASE_URL = "postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/appointment_db"

```

### 4. Running the Application

```bash
# Run from the root directory
uvicorn app.main:app --reload

```

The API will be available at `http://127.0.0.1:8000`.

---

## 📡 API Documentation

### Authentication

Protected routes require the following header:

* **Header Name**: `X-API-KEY`
* **Value**: `lnmiit-secret-key` (configurable in `app/auth.py`)

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
| --- | --- | --- | --- |
| `POST` | `/users/` | Register a new user (Client/Provider) | No |
| `DELETE` | `/users/{id}` | Remove a user | **Yes** |
| `POST` | `/appointments/` | Book a new slot | **Yes** |
| `GET` | `/appointments/{id}` | Get specific appointment details | No |
| `GET` | `/appointments/filter/date` | Filter appointments by `YYYY-MM-DD` | No |
| `PATCH` | `/appointments/{id}/cancel` | Cancel an appointment | **Yes** |
| `WS` | `/ws` | Real-time WebSocket update channel | No |

---

## 🧪 Testing

The project includes a suite of asynchronous tests using `pytest`.

**To run the tests:**

```bash
# Set PYTHONPATH to the current directory
export PYTHONPATH=$PYTHONPATH:. 
pytest tests/test_api.py

```

---

## 📁 Project Structure

```text
appointment_system/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app & WebSocket logic
│   ├── auth.py          # API Key Security
│   ├── database.py      # Async Engine & Session Generator
│   ├── models.py        # SQLAlchemy OOP Models
│   ├── schemas.py       # Pydantic Data Validation
│   └── decorators.py    # Custom Timing/Logging Decorators
├── tests/
│   ├── __init__.py
│   └── test_api.py      # Async Pytest suite
└── README.md

```

---

## 👨‍💻 Author

**Ojasvi Goyal** Data Scientist @Celebal Technologies | Machine Learning & NLP Focus
