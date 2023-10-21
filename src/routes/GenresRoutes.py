from flask import Blueprint, request, jsonify

import traceback

from src.validations_genres import *

# Logger
from src.utils.Logger import Logger

# Security
from src.utils.Security import Security
# Services
from src.services.GenreService import GenreService
# Model
from src.models.GenreModel import Genre

genres = Blueprint("genres", __name__)


@genres.route("/genres", methods=["GET"])
def list_genres():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            genres = GenreService.list_genres()
            if (len(genres) > 0):
                genres = [genre.__dict__ for genre in genres]
                return jsonify({'genres': genres, 'message': "genre list", 'success': True})

            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@genres.route("/genres/<id>", methods=["GET"])
def get_genre_by_id(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            genre = GenreService.get_genres_by_id(id)
            if genre != None:
                genre = (genre.__dict__)
                return jsonify({'genre': genre, 'message': "got genre", 'success': True})

            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@genres.route("/genres", methods=["POST"])
def add_genre():
    has_access = Security.verify_token(request.headers)

    if has_access:

        if validate_name(request.json["name"]):
            try:
                genre = GenreService.get_genres_by_id(request.json["name"])
                if genre != None:
                    return jsonify({"message": "Genre already exits, cannot be duplicated", "Success": False})
                else:
                    try:
                        name = request.json["name"]

                        genre = Genre(id, name)
                        created_genre = GenreService.add_genre(genre)

                        return jsonify({"message": 'genre created successfully', "success": True}), 201
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


@genres.route("/genres/<id>", methods=["DELETE"])
def delete_genre(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            genre = GenreService. get_genres_by_id(id)
            if genre != None:

                genre = GenreService.delete_genre(id)
                return jsonify({"message": "genre deleted", "success": True}), 204
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@genres.route("/genres/<id>", methods=["PUT"])
def update_genre(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        if validate_id(id) and (request.json["name"]):
            try:
                genre = GenreService.get_genres_by_id(id)
                if genre != None:
                    try:
                        name = request.json["name"]

                        genre = Genre(id, name)

                        updated_genre = GenreService.update_genre(id, genre)

                        return jsonify({"message": 'genre updated successfully', "success": True}), 201
                    except Exception as ex:
                        Logger.add_to_log("error", str(ex))
                        Logger.add_to_log("error", traceback.format_exc())
                else:
                    return jsonify({"message": "genre not found", "success": False})
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            return jsonify({"message": "Invalid parameters...", "success": False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
