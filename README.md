# FastAPI Hexagonal Architecture Example

This project demonstrates a FastAPI application built with a Hexagonal Architecture, suitable for a medical clinic's secretary system.

## Features

- Patient Registration
- Appointment Scheduling
- Appointment Rescheduling
- Appointment Cancellation

## Technologies

- FastAPI: Web framework for building APIs
- SQLAlchemy: ORM for database interactions
- Pydantic: Data validation and serialization
- PostgreSQL: Database

## Project Structure

```
app/
├── main.py
├── config.py
├── models/                 # Domain entities (pure business logic)
│   ├── patient.py
│   └── appointment.py
├── controller/             # Application layer (use cases)
│   ├── patientsBO.py
│   ├── appointmentBO.py
│   └── baseBO.py
├── adapters/                # External infrastructure
│   ├── postgresAdapter.py   # PostgreSQL adapter
│   ├── dbBase.py            # Base database operations
│   └── firestoreAdapter.py  # Firestore adapter
├── schemas/                # Pydantic schemas for request/response validation
│   ├── paciente_schema.py
│   └── consulta_schema.py
├── routers/                # FastAPI endpoints
│   ├── paciente_router.py
│   └── consulta_router.py
├── dependencies/           # Dependency injection container
│   └── container.py
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd fastapi_template
    ```

2.  **Create a virtual environment (recommended):
    ```bash
    uv sync
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv sync
    ```

4.  **Database Configuration:**
    This application uses PostgreSQL. You need to have a PostgreSQL server running.
    
    The database connection URL is configured in `app/config.py`.
    By default, it expects a PostgreSQL database at `postgresql://user:password@db:5432/clinic_db`.
    You can set the `DATABASE_URL` environment variable to override this.

    Example `.env` file (create this in the project root):
    ```
    DATABASE_URL="postgresql://your_user:your_password@your_db_host:5432/your_database_name"
    ```

5.  **Run the application:**
    ```bash
    cp app
    fastapi dev main.py
    ```

    The application will be accessible at `http://127.0.0.1:8000`.
    FastAPI automatically generates interactive API documentation at `http://127.0.0.1:8000/docs` (Swagger UI) and `http://127.0.0.1:8000/redoc` (ReDoc).