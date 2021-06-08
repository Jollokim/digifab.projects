import sqlite3

conn = sqlite3.connect("brukere.db")

c = conn.cursor()

c.execute("""CREATE TABLE brukere(
            username text NOT NULL UNIQUE,
            password text,
            age integer,
            PRIMARY KEY(username)
            )""")


# c.execute("INSERT INTO personer (username, password, age) VALUES (:username, :password, :age)", {"username": "Jollokim", "password": "12345", "age": 21})

conn.commit()

conn.close()
