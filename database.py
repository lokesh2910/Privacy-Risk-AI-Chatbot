import sqlite3


def init_db():

    conn = sqlite3.connect("chat_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_reply TEXT,
            risk TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_chat(user_message, bot_reply, risk):

    conn = sqlite3.connect("chat_logs.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(user_message, bot_reply, risk) VALUES (?, ?, ?)",
        (user_message, bot_reply, risk)
    )

    conn.commit()
    conn.close()