from flask import Flask, render_template, redirect, url_for, request
import pyodbc
from config import Config

app = Flask(__name__, template_folder='templates')

def get_db_connection():
    return pyodbc.connect(Config.AZURE_DATABASE_CONNECTION)

# Route for displaying the list of books
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', books=books)

# Route for adding a new book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        year = request.form['year']
        genre = request.form['genre']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, description, year, genre)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, description, year, genre))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

# Route for editing an existing book
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        year = request.form['year']
        genre = request.form['genre']

        cursor.execute("""
            UPDATE books
            SET title = ?, author = ?, description = ?, year = ?, genre = ?
            WHERE id = ?
        """, (title, author, description, year, genre, book_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    connection.close()

    if not book:
        return "Book not found", 404

    return render_template('edit_book.html', book=book)

# Route for deleting a book
@app.route('/delete/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

# Route for displaying book details
@app.route('/book/<int:book_id>')
def book_details(book_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    connection.close()

    if not book:
        return render_template('404.html'), 404

    return render_template('book_details.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
