from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False, unique=True)
    password = db.Column(db.String(200),nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    author = db.Column(db.String(80),nullable=False)
    genre = db.Column(db.String(20))
    isbn = db.Column(db.String(13),unique=True)
    status = db.Column(db.String(20),default="available")

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'),nullable=False)
    borrow_date = db.Column(db.Date,nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(20),default="borrowed")


