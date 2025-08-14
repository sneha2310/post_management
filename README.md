# 📬 Post Management System

A backend API for managing posts, built with **FastAPI**, **PostgreSQL**, and **Python ≥ 3.10**.  
The system supports CRUD operations for posts, authentication, and testing using `pytest`.

---

## 🚀 Tech Stack

- **Language:** Python ≥ 3.10
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** PostgreSQL
- **Testing:** [pytest](https://docs.pytest.org/)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/post-management-system.git
cd post-management-system
```
### 2. Create Virtual Environment & Install Dependencies
```commandline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```
### 3. Configure Environment Variables

Create a .env file in the root directory:
```commandline
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=test
DATABASE_PASSWORD=test
DATABASE_NAME=fastapi
SECRET_KEY=secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

### 4. Database Setup
Run Migrations

```commandline
alembic upgrade head
```

### 5. Running the Application
```commandline
uvicorn app.main:app --reload
```
Doc will be available at: http://127.0.0.1:8000/docs

### 6. Running Tests

We use pytest for automated testing.

```commandline
pytest -s  tests/test_posts.py  --disable-warnings
```

-v : detailed descriotion
-s : also prints the print statement
--disable-warnings: disable the warnings

### ⚠ Pytest Fixture Scope Issue

By default, pytest fixtures have scope="function".
This means the fixture runs once for every test function.

#### Problem:

In our test setup, the database fixture:

Deletes all data.

Recreates a fresh test database.

When running sequential tests (e.g., test_create_user → test_login_user),
the database was reset between tests.

This caused login tests to fail because the user created in the previous test was gone.

#### Attempted Fix: scope="module"

```commandline
    @pytest.fixture(scope="module")
    def test_session():
        # setup code here...
        yield session
        # teardown code here...
```

- scope="module" runs the fixture once per test file instead of per function.

- This prevented data loss between tests inside the same file.

- Downside: Tests became dependent on execution order and shared state,
which is considered bad practice because:

  - Tests should be independent and reproducible in isolation.

  - Module-scoped fixtures hide dependencies between tests.

#### Final Decision:

We kept scope="function" to maintain test independence.
Instead of relying on shared state between tests:

- Each test creates its own test data explicitly.

- This makes tests slower but more reliable and maintainable.

## 📂 Project Structure
```commandline
    post-management-system/
    │
    ├── app/
    │   ├── main.py           # FastAPI entry point
    │   ├── models.py         # SQLAlchemy models
    │   ├── routers/          # API route definitions
    │   ├── schemas.py        # Pydantic schemas
    │   ├── database.py       # DB connection setup
    │   └── tests/            # Test files
    │
    ├── alembic/              # Database migrations
    ├── requirements.txt
    ├── README.md
    └── .env
```
