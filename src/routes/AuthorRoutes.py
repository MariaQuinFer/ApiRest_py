from flask import Blueprint, request, jsonify
import traceback

from src.validations_authors import *

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.AuthorService import AuthorService
# Model
from src.models.AuthorModel import Author


authors = Blueprint("authors", __name__)


@authors.route("/authors", methods=["GET"])
def list_authors():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            authors = AuthorService.list_authors()
            if (len(authors) > 0):
                authors = [author.__dict__ for author in authors]
                return jsonify({'authors': authors, 'message': "authors list", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@authors.route("/authors/<id>", methods=["GET"])
def get_author_by_id(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            author = AuthorService.get_author_by_id(id)
            if author != None:
                author = (author.__dict__)
                return jsonify({'author': author, 'message': "got author", 'success': True})

            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@authors.route("/authors", methods=["POST"])
def add_author():
    has_access = Security.verify_token(request.headers)

    if has_access:

        if validate_name(request.json["nombre"]):
            try:
                author = AuthorService.get_author_by_id(request.json["nombre"])
                if author != None:
                    return jsonify({"message": "Author already exits, cannot be duplicated", "Success": False})
                else:
                    nombre = request.json["nombre"]

                    author = Author(id, nombre)
                    created_author = AuthorService.add_author(author)

                    return jsonify({"message": 'Author created successfully', "success": True}), 201
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            return jsonify({"message": "Invalid parameters...", "success": False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@authors.route("/authors/<id>", methods=["DELETE"])
def delete_author(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            author = AuthorService. get_author_by_id(id)
            if author != None:
                author = AuthorService.delete_author(id)
                return jsonify({"message": "Author deleted", "success": True}), 204
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@authors.route("/authors/<id>", methods=["PUT"])
def update_author(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        if validate_id(id) and (request.json["nombre"]):
            try:
                author = AuthorService.get_author_by_id(id)
                if author != None:
                    try:
                        nombre = request.json["nombre"]

                        author = Author(id, nombre)

                        updated_author = AuthorService.update_author(
                            id, author)

                        return jsonify({"message": 'Author updated successfully', "success": True}), 201
                    except Exception as ex:
                        Logger.add_to_log("error", str(ex))
                        Logger.add_to_log("error", traceback.format_exc())
                else:
                    return jsonify({"message": "Author not found", "success": False})
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            return jsonify({"message": "Invalid parameters...", "success": False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
