from flask import Blueprint, jsonify

from src.database.db import get_connection


carousel = Blueprint("carousel", __name__)


@carousel.route("/carousel", methods=['GET'])
def get_last_books():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
        SELECT l.id, l.portada, l.ISBN, a.nombre AS Author, l.titulo AS Title 
        FROM libros l
        JOIN autores a
        ON l.idAutor = a.id
        ORDER BY l.id DESC LIMIT 5
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        if data != None:
            # print(data)
            books = []
            for row in data:
                book = {
                    "id": row[0],
                    "portada": row[1],
                    "ISBN": row[2],
                    "Author": row[3],
                    "Title": row[4],
                }
                books.append(book)
            # print('libro:', book)
            # print('libros:', books)
            return jsonify({"books": books, "message": "Booksss list", "success": True})
        else:
            return None

    except Exception as ex:  # para atrapar cualquier error que pueda haber
        return jsonify({"message": "Error", "success": False})
