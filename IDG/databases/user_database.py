import sqlite3, hashlib

conn = sqlite3.connect("brukere.db")
c = conn.cursor()


# def createConn(database):
#     global conn, c
#     conn = sqlite3.connect("brukere.db")
#     c = conn.cursor()

class UserDatabase:

    def __init__(self):
        self.conn = sqlite3.connect("brukere.db")
        self.c = conn.cursor()

    def addUser(self, username, password, age):
        encPassword = hashlib.pbkdf2_hmac('sha512', bytes(password, "utf-8"), b'salt', 100_000).hex()
        with self.conn:
            try:
                c.execute("INSERT INTO brukere (username, password, age) VALUES (:username, :password, :age)",
                          {"username": username,
                           "password": encPassword,
                           "age": age})
            except sqlite3.IntegrityError:
                return False

        return True


    def getUserWithUsername(self, username):
        self.c.execute(f"SELECT * FROM brukere WHERE username = :username", {"username": username})
        return c.fetchall()


    def getAllUsers(self):
        self.c.execute("SELECT * FROM brukere")
        return c.fetchall()


    def ___removeAllUsers___(self):
        with self.conn:
            c.execute("DELETE FROM brukere")


    def getUserWithLogin(self, username, password):
        encPassword = hashlib.pbkdf2_hmac('sha512', bytes(password, "utf-8"), b'salt', 100_000).hex()
        self.c.execute(f"SELECT * FROM brukere WHERE username = :username AND password = :password", {"username": username, "password": encPassword})
        return c.fetchone()

    def __del__(self):
        self.conn.close()

