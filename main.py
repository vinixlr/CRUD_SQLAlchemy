from enum import unique
from types import MethodType
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)

#criando database com Sqlalchemye
class DataBaseCreate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)

#criando o database
""" db = sqlite3.connect("books-collection.db")
cursor = db.cursor()
 """




@app.route('/', methods=["POST", "GET"])
def home():
    books_list = db.session.query(DataBaseCreate).all()
    return render_template("index.html", book_list=books_list)

@app.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    book_id = id
    book_to_delete = DataBaseCreate.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data_form = request.form
        data_dict = {
                    "title": data_form["book_name"],
                     "author": data_form["book_author"],
                     "rating": float(data_form["rating"]) 
                    }

        new_book = DataBaseCreate(title=data_dict['title'], author=data_dict['author'], rating=data_dict['rating'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book = DataBaseCreate.query.filter_by(id=id).first()
    if request.method == "POST":
        data = request.form
        new_rating = float(data["rating"])
        book_to_update = DataBaseCreate.query.get(id)
        book_to_update.rating = new_rating
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('edit.html', book=book)



if __name__ == "__main__":
    app.run(debug=True)


# criando o banco de dados
""" cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)") """

""" cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit() """
