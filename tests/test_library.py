import pytest
import requests

@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000/"

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

def test_get_all_books(base_url, create_books):
    response = requests.get(base_url + 'books')
    assert response.status_code == 200
    assert len(response.json()) >= 3

def test_validate_all_books(base_url):
    response = requests.get(base_url + 'books')
    
    data = response.json()

    for book in data:
        assert 'id' in book
        assert isinstance(book['id'], int)
        
        assert 'title' in book
        assert isinstance(book['title'], str)
        
        assert 'author' in book
        assert isinstance(book['author'], str)
        
        assert 'genre' in book
        assert isinstance(book['genre'], str)
        
        assert 'rating' in book
        assert isinstance(book['rating'], float)
    


def test_get_specific_book(base_url, create_book):

    response = requests.get(base_url + f'books/{create_book}')

    assert response.status_code == 200




