from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CREATE DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"

db = SQLAlchemy(app)

class Author(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    nationality = db.Column(db.String, nullable = False)
    books = db.relationship('Book', backref='author_obj')

    def to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "nationality": self.nationality
        }


class Book(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)
    title = db.Column(db.String(50), nullable = False)
    author = db.Column(db.String(50), nullable = False)
    genre = db.Column(db.String(50), nullable = False)
    rating = db.Column(db.Float, nullable = False)
    

    def to_dictionary(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating
        }
    

with app.app_context():
    db.create_all()


# CREATE ROUTES

@app.route("/")
def home():
    return jsonify({"message": "Hello this is my Library API"})

# GET ALL BOOKS
@app.route("/books", methods = ["GET"])
def get_all_books():

    title = request.args.get("title")
    genre = request.args.get("genre")

    if title and genre:
        books = Book.query.filter_by(title=title, genre=genre).all()
    elif title:
        books = Book.query.filter_by(title=title).all()
    elif genre:
        books = Book.query.filter_by(genre=genre).all()
    else:
        books = Book.query.all()

    return jsonify([book.to_dictionary() for book in books])


# GET SPECIFIC BOOK BY ADDING ID
@app.route("/books/<int:book_id>", methods = ["GET"])
def get_specific_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book.to_dictionary())
    else:
        return jsonify({"Message": "Book with this id not found"}), 404
    
@app.route("/books", methods = ["GET"])
def get_all_books():

    genre = request.args.get("genre")

    if genre:
        books = Book.query.filter_by(genre=genre).all()
    else:
        books = Book.query.all()

    return jsonify([book.to_dictionary() for book in books])


# ADD BOOK TO THE LIBRARY
@app.route("/books", methods = ["POST"])
def add_new_book():
    data = request.get_json()

    if not all([data.get("title"), data.get("author"), data.get("genre"), data.get("rating")]):
        return jsonify({"error": "All fields are required"}), 400

    new_book = Book(title = data["title"],
                    author = data["author"],
                    genre = data["genre"],
                    rating = data["rating"])

    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dictionary()), 201

# UPDATE EXISTING BOOK
@app.route("/books/<int:book_id>", methods = ["PUT"])
def update_book(book_id):
    data = request.get_json()

    book = Book.query.get(book_id)

    if book:

        # VALIDATING THAT EVERYTHING WAS SENT 
        if not all([data.get("title"), data.get("author"), data.get("genre"), data.get("rating")]):
            return jsonify({"error": "All fields are required for PUT"}), 400

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.genre = data.get("genre", book.genre)
        book.rating = data.get("rating", book.rating)
        
        db.session.commit()
        
        return jsonify(book.to_dictionary())
    
    else:
        
        return jsonify({"Error message": "Book with this id doesnt exist"}), 404

# DELETE BOOK   
@app.route("/books/<int:book_id>", methods = ["DELETE"])
def delete_book(book_id):
    
    book = Book.query.get(book_id)

    if book:

        db.session.delete(book)
        db.session.commit()
        
        return jsonify({"Success": "Book was successfuly deleted"})
    
    else:
        
        return jsonify({"Error message": "Book doesnt exist"}), 404

# CHANGE PROPERTY VALUE OF CHOSEN BOOK   
@app.route("/books/<int:book_id>", methods = ["PATCH"])
def update_existing_book(book_id):

    data = request.get_json()

    book = Book.query.get(book_id)

    if book:

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.genre = data.get("genre", book.genre)
        book.rating = data.get("rating", book.rating)
        
        db.session.commit()
        
        return jsonify(book.to_dictionary())
    
    else:
        
        return jsonify({"Error message": "Book with this id doesnt exist"}), 404



if __name__ == "__main__":
    app.run(debug = True)


