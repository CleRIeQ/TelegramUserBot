import sqlite3


def create_table():
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()

    cur.execute("""

        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT)


    """)

    con.commit()
    con.close()


def add_new_user(user_nick):
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()

    try:
        cur.execute("""

            INSERT INTO user
            (nickname)
            VALUES
            (?) """, [user_nick])

        con.commit()
        con.close()

    except sqlite3.IntegrityError:
        con.commit()
        con.close()


def check_is_new(user_nick):
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()

    cur.execute(f"SELECT * FROM user WHERE nickname=?", (user_nick, ))
    row = cur.fetchone()

    con.commit()
    con.close()

    return row


def delete_all_rows():
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()

    cur.execute('DELETE FROM user;',)

    con.commit()
    con.close()
