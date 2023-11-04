# DataBase
from src.database.db import get_connection


class Lend():

    def __init__(self, id, idUser, ISBN, departury_date, return_date, action) -> None:
        self.id = id
        self.idUser = idUser
        self.ISBN = ISBN
        self.departury_date = departury_date
        self.return_date = return_date
        self.action = action

    def to_json(self):
        return {
            'id': self.id,
            'ISBN': self.idUser,
            'departury_date': self.departury_date,
            'return_date': self.return_date,
            'action': self.action
        }

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4])

    @staticmethod
    def lend_book(lend):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "call sp_lendBook({0},'{1}')".format(lend.idUser, lend.ISBN)
            cursor.execute(sql)
            sql = ("""
            UPDATE libros
            SET estado = "No disponible"
            WHERE ISBN = '{0}'
             """.format(lend.ISBN))
            cursor.execute(sql)
            # Confirm changes, updates from available to unavailable when the book is requested to be borrowed
            connection.commit()
            cursor.close()

    @staticmethod
    def delete_lend(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM prestamo WHERE id='{0}'".format(id)
            cursor.execute(sql)
            connection.commit()  # Confirm that a loan has been deleted

    @staticmethod
    def update_action(id, lend):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "call sp_updateLoan({0},'{1}')".format(id, lend.action)
            cursor.execute(sql)
            # Select the ISBN of the id entered in the previous query
            sql = ("SELECT ISBN FROM prestamo WHERE id = {0}".format(id))
            cursor.execute(sql)
            ISBN = cursor.fetchone()[0]
            print(ISBN)
            sql = (
                """UPDATE libros SET estado = "Disponible" WHERE ISBN = '{0}'""".format(ISBN))
            cursor.execute(sql)
            # Commit changes, updates from unavailable to available when the book is returned
            connection.commit()
            cursor.close
