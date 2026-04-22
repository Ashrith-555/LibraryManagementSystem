from backend.db_connection import connect
from datetime import date


def borrow_book(book_id, member_id):
    conn = connect()
    cur = conn.cursor()

    # Check book exists
    cur.execute(
        "SELECT avaliable FROM books WHERE book_id=?",
        (book_id,)
    )
    result = cur.fetchone()

    if result is None:
        conn.close()
        raise Exception("Book ID does not exist")

    # Check member exists
    cur.execute(
        "SELECT * FROM members WHERE member_id=?",
        (member_id,)
    )

    if cur.fetchone() is None:
        conn.close()
        raise Exception("Member ID does not exist")

    # Check availability
    if result[0] == 0:
        conn.close()
        raise Exception("Book already borrowed")

    # Insert loan record
    cur.execute(
        """
        INSERT INTO loans(book_id, member_id, issue_date, return_date)
        VALUES (?, ?, ?, NULL)
        """,
        (book_id, member_id, str(date.today()))
    )

    # Update book status
    cur.execute(
        "UPDATE books SET avaliable=0 WHERE book_id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()


def return_book(book_id, member_id):
    conn = connect()
    cur = conn.cursor()

    # Check active loan exists
    cur.execute(
        """
        SELECT * FROM loans
        WHERE book_id=? AND member_id=? AND return_date IS NULL
        """,
        (book_id, member_id)
    )

    if cur.fetchone() is None:
        conn.close()
        raise Exception("No active loan found")

    # Update return date
    cur.execute(
        """
        UPDATE loans
        SET return_date=?
        WHERE book_id=? AND member_id=? AND return_date IS NULL
        """,
        (str(date.today()), book_id, member_id)
    )

    # Make book available again
    cur.execute(
        "UPDATE books SET avaliable=1 WHERE book_id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()