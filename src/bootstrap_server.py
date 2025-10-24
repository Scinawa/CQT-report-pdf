import sqlite3
import argparse


def init_db():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists.")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap server database.")
    parser.add_argument(
        "--init-db", action="store_true", help="Initialize the database."
    )
    parser.add_argument(
        "--add-user", nargs=2, metavar=("USERNAME", "PASSWORD"), help="Add a new user."
    )

    args = parser.parse_args()

    if args.init_db:
        init_db()
    elif args.add_user:
        username, password = args.add_user
        add_user(username, password)
    else:
        parser.print_help()
