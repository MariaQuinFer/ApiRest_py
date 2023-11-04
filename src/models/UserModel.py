# DataBase
from src.database.db import get_connection


class User():

    def __init__(self, id, username, email, password, fullname, usertype) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.fullname = fullname
        self.usertype = usertype

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'fullname': self.fullname,
            'usertype': self.usertype
        }

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4], row[5])

    @staticmethod
    def list_users():
        connecton = get_connection()
        with connecton.cursor() as cursor:
            cursor.execute("""
                           SELECT *
                           FROM users
                           """)
            data = cursor.fetchall()
            return [User.from_row(row) for row in data]

    @staticmethod
    def get_user_by_id(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
            SELECT *
            FROM users 
            WHERE id = {0}
            """.format(id)
            cursor.execute(sql)

            data = cursor.fetchone()
            if data != None:
                return User.from_row(data)
            else:
                return None

    @staticmethod
    def delete_user(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM users WHERE id='{0}'".format(id)
            cursor.execute(sql)
            connection.commit()  # Confirm that a user has been deleted

    @staticmethod
    def update_usertype(id, user):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                UPDATE users
                SET usertype = '{0}'
                WHERE id = {1}
            """.format(user.usertype, id)
            cursor.execute(sql)
            connection.commit()  # Confirms the action of modifying the usertype of a user

    @staticmethod
    def update_password(id, user):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "call sp_updatePassword({0},'{1}')".format(id, user.password)
            cursor.execute(sql)
            connection.commit()  # Confirms the action of modifying the usertype of a user
