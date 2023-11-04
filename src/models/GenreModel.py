from src.database.db import get_connection


class Genre():
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
    def list_genres():
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT * 
            FROM genres
            """)
            data = cursor.fetchall()
            return [Genre.from_row(row) for row in data]

    @staticmethod
    def get_genre_by_id(id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
            SELECT *
            FROM genres
            WHERE id = '{0}'
            """.format(id)
            cursor.execute(sql)

            data = cursor.fetchone()
            if data != None:
                return Genre.from_row(data)
            else:
                return None

    @staticmethod
    def add_genre(genre):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            INSERT INTO genres (name)
            VALUES ('{0}')
        """.format(genre.name)
        cursor.execute(sql)
        connection.commit()  # Confirm the action of adding genre

    @staticmethod
    def delete_genre(id):
        connection = get_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM genres WHERE id='{0}'".format(id)
        cursor.execute(sql)
        connection.commit()  # Confirm that a genre has been removed

    @staticmethod
    def update_genre(id, genre):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE genres
            SET name = '{}'
            WHERE id = {}
        """.format(genre.name, id)
        cursor.execute(sql)
        connection.commit()  # Confirms the action of modifying a genre
