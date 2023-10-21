from flask import Blueprint, request, jsonify

import traceback

from src.validations_editorials import *

# Logger
from src.utils.Logger import Logger

# Security
from src.utils.Security import Security
# Services
from src.services.EditorialService import EditorialService
# Model
from src.models.EditorialModel import Editorial

editorials = Blueprint('editorials', __name__)


@editorials.route("/editorials", methods=["GET"])
def list_editorials():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            editorials = EditorialService.list_editorials()
            if (len(editorials) > 0):
                editorials = [editorial.__dict__ for editorial in editorials]
                return jsonify({'editorials': editorials, 'message': "editorials list", 'success': True})

            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@editorials.route("/editorials/<id>", methods=["GET"])
def get_editorial_by_id(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            editorial = EditorialService.get_editorial_by_id(id)
            if editorial != None:
                editorial = (editorial.__dict__)
                return jsonify({'editorial': editorial, 'message': "got editorial", 'success': True})

            else:
                return jsonify({'message': "Not Found", 'success': True})

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@editorials.route("/editorials", methods=["POST"])
def add_editorial():
    has_access = Security.verify_token(request.headers)

    if has_access:
        if validate_name(request.json["name"]):
            try:
                editorial = EditorialService.get_editorial_by_id(
                    request.json["name"])
                if editorial != None:
                    return jsonify({"message": "Editorial already exits, cannot be duplicated", "Success": False})
                else:
                    try:
                        name = request.json["name"]
                        editorial = Editorial(id, name)
                        created_editorial = EditorialService.add_editorial(
                            editorial)

                        return jsonify({"message": 'Editorial created successfully', "success": True}), 201
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


@editorials.route("/editorials/<id>", methods=["DELETE"])
def delete_editorial(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            editorial = EditorialService. get_editorial_by_id(id)
            if editorial != None:

                editorial = EditorialService.delete_editorial(id)
                return jsonify({"message": "Author deleted", "success": True}), 204
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@editorials.route("/editorials/<id>", methods=["PUT"])
def update_editorial(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        if validate_id(id) and (request.json["name"]):
            try:
                editorial = EditorialService.get_editorial_by_id(id)
                if editorial != None:
                    try:
                        name = request.json["name"]

                        editorial = Editorial(id, name)

                        updated_editorial = EditorialService.update_editorial(
                            id, editorial)

                        return jsonify({"message": 'Editorial updated successfully', "success": True}), 201
                    except Exception as ex:
                        Logger.add_to_log("error", str(ex))
                        Logger.add_to_log("error", traceback.format_exc())
                else:
                    return jsonify({"message": "Editorial not found", "success": False})
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            return jsonify({"message": "Invalid parameters...", "success": False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
