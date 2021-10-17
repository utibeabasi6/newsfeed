import sqlite3

DATABASE_FILE = '../database.db'


class Database(object):
    def __init__(self):
        """
        Creates all database tables if they do not exist when the database is initialized for the first time
        """
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Users (username text, password text)')
        conn.commit()
        conn.close()

    def add_user(self, username, password):
        """
        Adds a new user to the database if user does not already exists
        Returns True if user has been successfully added to the database else False
        :param username: string
        :param password: string
        :return: bool
        """

        conn = sqlite3.connect(DATABASE_FILE)
        user_exists = self.check_username(username)  # Check if the user already exists in the database table
        if not user_exists:
            c = conn.cursor()
            c.execute('INSERT INTO Users values(?, ?)', (username, password))
            conn.commit()
            conn.close()
            return True
        return False

    def check_user(self, username, password):
        """
        Checks if a user exists in a database returns True if user exists else False
        :param password: string
        :param username: string
        :return: bool
        """
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('SELECT * FROM Users WHERE username=? and password=?', (username, password))
        if len(c.fetchall()) > 0:
            return True
        conn.commit()
        conn.close()
        return False

    def check_username(self, username):
        """
        Checks if a user exists in a database returns True if user exists else False
        :param username: string
        :return: bool
        """
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('SELECT * FROM Users WHERE username=?', (username,))
        if len(c.fetchall()) > 0:
            return True
        conn.commit()
        conn.close()
        return False