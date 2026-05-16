import pytest
import requests

# FIXTURE OF URLFOR TESTING PURPOSES

@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000/"

# FIXTURE FOR CREATING AUTHOR

@pytest.fixture
def create_author(base_url):

    payload = {
        "name": "Daniel Hevier",
        "nationality": "Slovakia"
    }

    response = requests.post(base_url + "authors", json = payload)
    author_id = response.json()["id"]

    yield author_id

    requests.delete(base_url + f"authors/{author_id}")

# FIXTURE FOR CREATING A BOOK

@pytest.fixture
def create_book(base_url):
    payload = {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "rating": 4.8
    }
    response = requests.post(base_url + "books", json=payload)
    book_id = response.json()["id"]
    
    yield book_id

    requests.delete(base_url + f"books/{book_id}")

# FIXTURE FOR CREATING 3 BOOKS TO USE FOR TESTING

@pytest.fixture
def create_books(base_url):
    books = [
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 4.8},
        {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "rating": 4.7},
        {"title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "rating": 4.5}
    ]
    ids = []
    for book in books:
        response = requests.post(base_url + "books", json=book)
        ids.append(response.json()["id"])

    yield ids
    
    for book_id in ids:
        requests.delete(base_url + f"books/{book_id}")