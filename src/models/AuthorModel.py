# Database
from src.database.db import get_connection


class Author():

    def __init__(self, id, nombre) -> None:
        self.id = id
        self.nombre = nombre

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
        }

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1])

    @staticmethod
    def list_authors():
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT * 
            FROM autores
            """)
            data = cursor.fetchall()
            return [Author.from_row(row) for row in data]

    @staticmethod
    def get_author_by_id(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
            SELECT *
            FROM autores 
            WHERE id = '{0}'
            """.format(id)
            cursor.execute(sql)

            data = cursor.fetchone()
            if data != None:
                return Author.from_row(data)
            else:
                return None

    @staticmethod
    def add_author(author):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            INSERT INTO autores (nombre)
            VALUES ('{0}')
        """.format(author.nombre)
        cursor.execute(sql)
        connection.commit()  # Confirma la accion de añadir autor

    @staticmethod
    def delete_author(id):
        connection = get_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM autores WHERE id='{0}'".format(id)
        cursor.execute(sql)
        connection.commit()  # Confirma que se ha eliminado un autor

    @staticmethod
    def update_author(id, author):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE autores
            SET nombre = '{0}'
            WHERE id = {1}
        """.format(author.nombre, id)
        cursor.execute(sql)
        connection.commit()  # Confirma la accion de añadir autor
