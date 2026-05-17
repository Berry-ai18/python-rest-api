import pytest
import requests


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

def test_get_all_authors(base_url, create_author):
    response = requests.get(base_url + "authors")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_one_author(base_url,create_author):
    response = requests.get(base_url + f"authors/{create_author}")
    assert response.status_code == 200
    assert 'name' in response.json()
    assert 'nationality' in response.json()

def test_get_invalid_author_id(base_url, create_author):
    response = requests.get(base_url + "authors/90999")
    assert response.status_code == 404

def test_create_author(base_url):
    response = requests.post(base_url + "authors", json = {"name": "Maria Razusova Martakova", "nationality": "Slovakia"})
    assert response.status_code == 201
    data = response.json()
    assert 'name' in data
    assert 'nationality' in data
    requests.delete(base_url + f"authors/{data['id']}")

def test_create_author_no_name(base_url):
    response = requests.post(base_url + "authors", json = {"name": "Palo Habera"})
    assert response.status_code == 400

def test_delete_author(base_url, create_author):
    response = requests.delete(base_url + f"authors/{create_author}")
    assert response.status_code == 200
    verify = requests.get(base_url + f'authors/{create_author}')
    assert verify.status_code == 404

def test_delete_author_wrongid(base_url):
    response = requests.delete(base_url + "authors/49949")
    assert response.status_code == 404


