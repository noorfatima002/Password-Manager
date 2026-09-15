import sqlite3

DATABASE_NAME = "passwords.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_password(website, username, password):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )

    connection.commit()
    connection.close()


def get_passwords():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM passwords")
    records = cursor.fetchall()

    connection.close()
    return records


def search_passwords(website):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM passwords WHERE website LIKE ?",
        ('%' + website + '%',)
    )

    records = cursor.fetchall()

    connection.close()
    return records


def update_password(record_id, website, username, password):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE passwords
        SET website = ?, username = ?, password = ?
        WHERE id = ?
        """,
        (website, username, password, record_id)
    )

    connection.commit()
    connection.close()


def delete_password(record_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM passwords WHERE id = ?",
        (record_id,)
    )

    connection.commit()
    connection.close()