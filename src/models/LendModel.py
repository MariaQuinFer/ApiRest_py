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
    # Confirmar los cambios en la base de datos
            connection.commit()
    # Cerrar el cursor
            cursor.close()

    @staticmethod
    def delete_lend(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM prestamo WHERE id='{0}'".format(id)
            cursor.execute(sql)
            connection.commit()  # Confirma que se ha eliminado un prestamo

    @staticmethod
    def update_action(id, lend):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "call sp_updateLoan({0},'{1}')".format(id, lend.action)
            cursor.execute(sql)
            sql = ("SELECT ISBN FROM prestamo WHERE id = {0}".format(id))
            cursor.execute(sql)
            ISBN = cursor.fetchone()[0]
            print(ISBN)
            sql = (
                """UPDATE libros SET estado = "Disponible" WHERE ISBN = '{0}'""".format(ISBN))
            cursor.execute(sql)
            connection.commit()
            cursor.close
