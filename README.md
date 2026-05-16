# Python REST API — Library

A simple REST API built with Flask and SQLAlchemy to manage a book library.
Built to understand Python backend development and practice API testing with pytest.

## Tech Stack

- Python / Flask
- SQLAlchemy / SQLite
- pytest / requests

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /books | Get all books |
| GET | /books/{id} | Get book by ID |
| POST | /books | Add a new book |
| PUT | /books/{id} | Update all fields |
| PATCH | /books/{id} | Update specific fields |
| DELETE | /books/{id} | Delete a book |

## How to Run

```bash
# Create and activate virtual environment
python -m venv api_env
api_env\Scripts\activate  # Windows
source api_env/bin/activate  # Mac

# Install dependencies
pip install -r requirements.txt

# Run the API
python library/library.py
```

## How to Run Tests

Make sure the API is running, then:

```bash
pytest tests/
```