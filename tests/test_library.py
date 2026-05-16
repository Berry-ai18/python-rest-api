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


# GET ALL BOOKS 
def test_get_all_books(base_url, create_books):
    response = requests.get(base_url + 'books')
    assert response.status_code == 200
    assert len(response.json()) >= 3


# VALIDATE THAT THERE ARE CORRECT PROPERTIES IN RESPONSE
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
    

# USING GET METHOD TO GET SPECIFIC BOOK
def test_get_specific_book(base_url, create_book):

    response = requests.get(base_url + f'books/{create_book}')

    assert response.status_code == 200

def test_get_invalid_book(base_url, create_books):
    response = requests.get(base_url + 'books/9999')
    assert response.status_code == 404

def test_post_book(base_url):
    payload = {
        'title':'Crazy',
        'author': 'Pato',
        'genre':'drama',
        'rating': '3.5'
    }

    response = requests.post(base_url + 'books', json = payload)
    assert response.status_code == 201
    data = response.json()
    assert 'Crazy' in data['title']

    requests.delete(base_url + f"books/{data['id']}")


def test_post_book_notitle(base_url):
    payload = {
        'author': 'Pato',
        'genre':'drama',
        'rating': '3.5'
    }

    response = requests.post(base_url + 'books', json = payload)
    assert response.status_code == 400

def test_post_book_incorrect_rating(base_url):
    payload = {
        'title':'Crazy',
        'author': 'Pato',
        'genre':'drama',
        'rating': 'STRING INSTEAD OF FLOAT'
    }

    response = requests.post(base_url + 'books', json = payload)
    assert response.status_code == 400


def test_put_book(base_url, create_book):
    payload = {
        'title':'Crazy',
        'author': 'Pato',
        'genre':'drama',
        'rating': '3.4'
    }

    response = requests.put(base_url + f'books/{create_book}', json = payload)
    assert response.status_code == 200

def test_put_book_norating(base_url, create_book):
    payload = {
        'title':'Crazy',
        'author': 'Pato',
        'genre':'drama',
    }

    response = requests.put(base_url + f'books/{create_book}', json = payload)
    assert response.status_code == 400

def test_put_book_invalidid(base_url):
    payload = {
        'title':'Crazy',
        'author': 'Pato',
        'genre':'drama',
        'rating': '3.4'
    }

    response = requests.put(base_url + f'books/5059', json = payload)
    assert response.status_code == 404


def test_patch_method(base_url, create_book):
    response = requests.patch(base_url + f"books/{create_book}", json = {"title": "Hangover"})
    assert response.status_code == 200
    data = response.json()
    assert 'title' in data
    assert 'Hangover' in data['title']

def test_patch_method_invalid(base_url):
    response = requests.patch(base_url + f"books/549045", json = {"title": "Hangover"})
    assert response.status_code == 404

def test_delete_book(base_url, create_book):
    response = requests.delete(base_url + f'books/{create_book}')
    assert response.status_code == 200

    # Verify book is actually gone
    verify = requests.get(base_url + f'books/{create_book}')
    assert verify.status_code == 404


def test_delete_book_invalidid(base_url):
    response = requests.delete(base_url + f'books/40439')
    assert response.status_code == 404
