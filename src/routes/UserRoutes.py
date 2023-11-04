from flask import Blueprint, request, jsonify
import traceback

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.UserService import UserService
# Model
from src.models.UserModel import User


users = Blueprint("users", __name__)


@users.route("/users", methods=["GET"])
def list_users():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            users = UserService.list_users()
            if (len(users) > 0):
                users = [user.__dict__ for user in users]
                return jsonify({'users': users, 'message': "users list", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@users.route("/users/<id>", methods=["GET"])
def get_user_by_id(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            user = UserService.get_user_by_id(id)
            if user != None:
                user = (user.__dict__)
                return jsonify({'user': user, 'message': "got user", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@users.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            user = UserService.get_user_by_id(id)
            if user != None:
                user = UserService.delete_user(id)
                return jsonify({"message": "User deleted", "success": True}), 204
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@users.route("/users/<id>", methods=["PUT"])
def update_usertype(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            user = UserService.get_user_by_id(id)
            if user != None:
                try:
                    usertype = request.json["usertype"]

                    user = User(id, None, None, None, None, usertype)

                    updated_usertype = UserService.update_usertype(
                        id, user)

                    return jsonify({"message": 'User updated successfully', "success": True}), 201
                except Exception as ex:
                    Logger.add_to_log("error", str(ex))
                    Logger.add_to_log("error", traceback.format_exc())
            else:
                return jsonify({"message": "user not found", "success": False})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
