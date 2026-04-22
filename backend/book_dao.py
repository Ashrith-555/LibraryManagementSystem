from backend.db_connection import connect

def add_book(title, author, isbn):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO books(title, author, isbn) VALUES (?, ?, ?)",
                (title, author, isbn))
    conn.commit()
    conn.close()


def get_books():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    data = cur.fetchall()
    conn.close()
    return data


def delete_book(book_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()


def update_book(book_id, title, author, isbn):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE books SET title=?, author=?, isbn=? WHERE book_id=?",
        (title, author, isbn, book_id)
    )

    conn.commit()
    conn.close()


# NEW (needed for partial update)
def get_book_by_id(book_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
    data = cur.fetchone()

    conn.close()
    return data


# SEARCH FUNCTION
def search_books(keyword):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM books
        WHERE 
            title LIKE ? OR
            author LIKE ? OR
            isbn LIKE ? OR
            book_id LIKE ?
    """, (
        '%' + keyword + '%',
        '%' + keyword + '%',
        '%' + keyword + '%',
        '%' + keyword + '%'
    ))

    data = cur.fetchall()
    conn.close()
    return data