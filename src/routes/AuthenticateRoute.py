from flask import Blueprint, request, jsonify
from decouple import config

import traceback
import datetime
import jwt

from src.database.db import get_connection

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Modal
from src.models.UserModel import User
# Service
from src.services.UserService import UserService


main = Blueprint("autorization", __name__)


def authenticate(username, password):
    # Search for the user by username in the database
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "call sp_verifyLogin(%s, %s)"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        cursor.close()
    # If the user exists and the password matches, generate a JWT token with their information and an expiration date
    if user and user[3] == password:
        token = jwt.encode({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'fullname': user[4],
            'usertype': user[5],
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, config('JWT_KEY'), algorithm="HS256")
        return token
    # Si no, devolver None
    else:
        return None


def verify_token(token):
    # Try to decode JWT token with application secret
    try:
        data = jwt.decode(
            token, config('JWT_KEY'), algorithms=["HS256"])
        # Find the user by their id in the database
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT id, username, email, fullname, usertype FROM users WHERE id = %s"
            cursor.execute(sql, (data['id'],))
            user = cursor.fetchone()
            cursor.close()
        # If the user exists, return their information
        if user:
            return {("current_client"): {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'fullname': user[3],
                'usertype': user[4]
            }, "logged_in": True}
        # If not, return None
        else:
            return {"logged_in": False}
    # If any error occurs while decoding the JWT token, return None
    except Exception as ex:
        Logger.add_to_log("error132", str(ex))
        Logger.add_to_log("error133", traceback.format_exc())


# Route to register a new user in the database
@main.route('/register', methods=['POST'])
def register():
    try:
        # Get user data from request body
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')
        # Validate that the data is not empty
        if not username or not email or not password:
            return jsonify({'message': 'Faltan datos'}), 400
        # Validate that the username is not registered
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT username FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user_username = cursor.fetchone()
            cursor.close()
        if user_username:
            return jsonify({'message': 'El nombre de usuario ya está registrado'}), 202
        # Validate that the email is not registered
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT email FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user_mail = cursor.fetchone()
            cursor.close()
        if user_mail:
            return jsonify({'message': 'El correo electrónico ya está registrado'}), 203
        # Insert the new user into the database
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = 'call sp_addUser(%s, %s, %s, %s)'
            cursor.execute(sql, (username, email, password, fullname))
            connection.commit()
            cursor.close()
        # Return a success message
            return jsonify({'message': 'Usuario registrado correctamente'}), 201
    except Exception as ex:
        Logger.add_to_log("error132", str(ex))
        Logger.add_to_log("error133", traceback.format_exc())


# Route to change password
@main.route('/register/<id>', methods=['PUT'])
def update_password(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            user = UserService.get_user_by_id(id)
            if user != None:
                try:
                    password = request.json["password"]

                    user = User(id, None, None, password, None, None)

                    updated_user = UserService.update_password(id, user)

                    return jsonify({"message": 'User updated successfully', "success": True}), 201
                except Exception as ex:
                    Logger.add_to_log("error132", str(ex))
                    Logger.add_to_log("error133", traceback.format_exc())
            else:
                return jsonify({"message": "user not found", "success": False})
        except Exception as ex:
            Logger.add_to_log("error137", str(ex))
            Logger.add_to_log("error138", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


# Route to log in with a user and get a JWT token
@main.route('/login', methods=['POST'])
def login():
    try:
        # Get user data from request body
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # Validate that the data is not empty
        if not username or not password:
            return jsonify({'message': 'Faltan datos'}), 400
        # Authenticate the user with their email and password and generate a JWT token
        token = authenticate(username, password)
        # If the token is valid, return it to the user
        if token:
            return jsonify({'token': token}), 200
        # If not, return an error message
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 202
    except Exception as ex:
        Logger.add_to_log("error132", str(ex))
        Logger.add_to_log("error133", traceback.format_exc())


# Route to get the user profile from a JWT token
@main.route('/profile', methods=['GET'])
def profile():
    try:
        # Get JWT token from request header
        auth_header = request.headers.get('Authorization')
        # Validate that the token exists and is in the correct format
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Falta el token'}), 401
        token = auth_header.split()[1]
        # Verify JWT token and get user information
        user = verify_token(token)
        # If the user is valid, return their information
        if user:
            return jsonify(user), 200
        # If not, return an error message
        else:
            return jsonify({'message': 'Token inválido o expirado, inicia sesión para continuar.'}), 401
    except Exception as ex:
        Logger.add_to_log("error132", str(ex))
        Logger.add_to_log("error133", traceback.format_exc())
