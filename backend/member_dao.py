from backend.db_connection import connect


def add_member(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO members(name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()
    conn.close()


def get_members():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM members")
    data = cur.fetchall()

    conn.close()
    return data


def delete_member(member_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM members WHERE member_id=?",
        (member_id,)
    )

    conn.commit()
    conn.close()


# UPDATE ONLY FILLED VALUES
def update_member(member_id, name, phone):
    conn = connect()
    cur = conn.cursor()

    # Get old data first
    cur.execute(
        "SELECT name, phone FROM members WHERE member_id=?",
        (member_id,)
    )

    old = cur.fetchone()

    if old is None:
        conn.close()
        return False

    new_name = name if name.strip() != "" else old[0]
    new_phone = phone if phone.strip() != "" else old[1]

    cur.execute(
        "UPDATE members SET name=?, phone=? WHERE member_id=?",
        (new_name, new_phone, member_id)
    )

    conn.commit()
    conn.close()
    return True