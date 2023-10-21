from flask import Blueprint, request, jsonify

import traceback

from src.validations_books import *

# Logger
from src.utils.Logger import Logger

# Security
from src.utils.Security import Security
# Services
from src.services.BookService import BookService
# Models
from src.models.BookModel import Book


books = Blueprint("books", __name__)


@books.route("/books", methods=["GET"])
def list_books():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            books = BookService.list_books()
            if (len(books) > 0):
                books = [book.__dict__ for book in books]
                return jsonify({'books': books, 'message': "book list", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@books.route("/books/<ISBN>", methods=["GET"])
def read_book(ISBN):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            book = BookService.read_booK_by_id(ISBN)
            if book != None:
                book = (book.__dict__)
                return jsonify({'book': book, 'message': "got book", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@books.route("/books", methods=["POST"])
def add_book():
    has_access = Security.verify_token(request.headers)

    if has_access:

        if (
            validate_ISBN(request.json["ISBN"])
            and validate_title(request.json["titulo"])
            and validate_idAuthor(request.json["idAutor"])
            and validate_idGenre(request.json["idGenre"])
            and validate_idEditorial(request.json["idEditorial"])
            and validate_language(request.json["idioma"])
            and validate_pages(request.json["paginas"])
            and validate_cover(request.json["portada"])
            and validate_description(request.json["descripcion"])
        ):
            try:
                book = BookService.read_booK_by_id(request.json["ISBN"])
                if book != None:
                    return jsonify({"message": "ISBN already exits, cannot be duplicated", "exito": False})
                else:
                    try:
                        ISBN = request.json["ISBN"]
                        titulo = request.json["titulo"]
                        idAutor = request.json["idAutor"]
                        idGenre = request.json["idGenre"]
                        idEditorial = request.json["idEditorial"]
                        idioma = request.json["idioma"]
                        paginas = request.json["paginas"]
                        portada = request.json["portada"]
                        descripcion = request.json["descripcion"]
                        estado = request.json["estado"]

                        book = Book(id, ISBN, titulo, idAutor, idGenre,
                                    idEditorial, idioma, paginas, portada, descripcion, estado)
                        created_book = BookService.create_book(book)

                        return jsonify({"message": 'Book created successfully', "success": True}), 201
                    except Exception as ex:
                        Logger.add_to_log("error", str(ex))
                        Logger.add_to_log("error", traceback.format_exc())
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            return jsonify({"message": "Invalid parameters...", "success": False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@books.route("/books/<ISBN>", methods=["DELETE"])
def delete_book(ISBN):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            book = BookService.read_booK_by_id(ISBN)
            if book != None:

                book = BookService.delete_book(ISBN)
                return jsonify({"message": "Book deleted", "success": True}), 204
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@books.route("/books/<ISBN>", methods=["PUT"])
def update_book(ISBN):
    has_access = Security.verify_token(request.headers)

    if has_access:

        if (
            validate_ISBN(request.json["ISBN"])
            and validate_title(request.json["titulo"])
            and validate_idAuthor(request.json["idAutor"])
            and validate_idGenre(request.json["idGenre"])
            and validate_idEditorial(request.json["idEditorial"])
            and validate_language(request.json["idioma"])
            and validate_pages(request.json["paginas"])
            and validate_cover(request.json["portada"])
            and validate_description(request.json["descripcion"])
        ):
            try:
                book = BookService.read_booK_by_id(request.json["ISBN"])
                if book != None:
                    try:
                        ISBN = request.json["ISBN"]
                        titulo = request.json["titulo"]
                        idAutor = request.json["idAutor"]
                        idGenre = request.json["idGenre"]
                        idEditorial = request.json["idEditorial"]
                        idioma = request.json["idioma"]
                        paginas = request.json["paginas"]
                        portada = request.json["portada"]
                        descripcion = request.json["descripcion"]
                        estado = request.json["estado"]

                        book = Book(id, ISBN, titulo, idAutor, idGenre, idEditorial,
                                    idioma, paginas, portada, descripcion, estado)
                        update_book = BookService.update_book(ISBN, book)

                        return jsonify({"message": 'Book updated successfully', "success": True}), 201
                    except Exception as ex:
                        Logger.add_to_log("error", str(ex))
                        Logger.add_to_log("error", traceback.format_exc())
                else:
                    return jsonify({"message": "Book not found", "success": False})
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            return jsonify({"message": "Invalid parameters...", "success": False}), 205
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
