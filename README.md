# Python REST API — Library

A simple REST API built with Flask and SQLAlchemy to manage a book library with authors.
Built to understand Python backend development and practice API testing with pytest.

## Tech Stack

- Python / Flask
- SQLAlchemy / SQLite
- pytest / requests

## Endpoints

### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /books | Get all books (supports ?title= and ?genre= filters) |
| GET | /books/{id} | Get book by ID |
| POST | /books | Add a new book |
| PUT | /books/{id} | Update all fields |
| PATCH | /books/{id} | Update specific fields |
| DELETE | /books/{id} | Delete a book |

### Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /authors | Get all authors (supports ?name= and ?nationality= filters) |
| GET | /authors/{id} | Get author by ID including their books |
| POST | /authors | Add a new author |
| DELETE | /authors/{id} | Delete an author |

## How to Run

```bash
# Create and activate virtual environment
python -m venv api_env
api_env\Scripts\activate  # Windows
source api_env/bin/activate  # Mac

# Install dependencies
pip install -r requirements.txt

# Run the API
python library.py
```

## How to Run Tests

Make sure the API is running, then:

```bash
pytest tests/
```