from flask import Blueprint, jsonify

from src.database.db import get_connection


carousel = Blueprint("carousel", __name__)

# Unprotected route to put in the books carousel, where the last 5 ids added to the books table will be shown


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
            return jsonify({"books": books, "message": "Booksss list", "success": True})
        else:
            return None

    except Exception as ex:  # para atrapar cualquier error que pueda haber
        return jsonify({"message": "Error", "success": False})
