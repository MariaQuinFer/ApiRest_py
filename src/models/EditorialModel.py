from src.database.db import get_connection


class Editorial():

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1])

    @staticmethod
    def list_editorials():
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT * 
            FROM editorials
            """)
            data = cursor.fetchall()
            return [Editorial.from_row(row) for row in data]

    @staticmethod
    def get_editorial_by_id(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
            SELECT *
            FROM editorials
            WHERE id = '{0}'
            """.format(id)
            cursor.execute(sql)

            data = cursor.fetchone()
            if data != None:
                return Editorial.from_row(data)
            else:
                return None

    @staticmethod
    def add_editorial(editorial):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            INSERT INTO editorials (name)
            VALUES ('{0}')
        """.format(editorial.name)
        cursor.execute(sql)
        connection.commit()  # Confirma la accion de añadir libro

    @staticmethod
    def delete_editorial(id):
        connection = get_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM editorials WHERE id='{0}'".format(id)
        cursor.execute(sql)
        connection.commit()  # Confirma que se ha eliminado un libro

    @staticmethod
    def update_editorial(id, editorial):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE editorials
            SET name = '{0}'
            WHERE id = {1}
        """.format(editorial.name, id)
        cursor.execute(sql)
        connection.commit()  # Confirma la accion de añadir autor
