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
    # Buscar al usuario por su nombre se usuario en la base de datos
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "call sp_verifyLogin(%s, %s)"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        cursor.close()
    # Si el usuario existe y la contraseña coincide, generar un token JWT con su información y una fecha de expiración
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
    # Intentar decodificar el token JWT con el secreto de la aplicación
    try:
        data = jwt.decode(
            token, config('JWT_KEY'), algorithms=["HS256"])
        # Buscar al usuario por su id en la base de datos
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT id, username, email, fullname, usertype FROM users WHERE id = %s"
            cursor.execute(sql, (data['id'],))
            user = cursor.fetchone()
            cursor.close()
        # Si el usuario existe, devolver su información
        if user:
            return {("current_client"): {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'fullname': user[3],
                'usertype': user[4]
            }, "logged_in": True}
        # Si no, devolver None
        else:
            return {"logged_in": False}
    # Si ocurre algún error al decodificar el token JWT, devolver None
    except Exception as e:
        return None


# Ruta para registrar un nuevo usuario en la base de datos
@main.route('/register', methods=['POST'])
def register():
    # Obtener los datos del usuario del cuerpo de la solicitud
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    fullname = data.get('fullname')
    # Validar que los datos no estén vacíos
    if not username or not email or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    # Validar que el nombre de usuario no esté registrado
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT username FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        user_username = cursor.fetchone()
        cursor.close()
    if user_username:
        return jsonify({'message': 'El nombre de usuario ya está registrado'}), 202
    # Validar que el correo electrónico no esté registrado
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT email FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        user_mail = cursor.fetchone()
        cursor.close()
    if user_mail:
        return jsonify({'message': 'El correo electrónico ya está registrado'}), 203
    # Insertar el nuevo usuario en la base de datos
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = 'call sp_addUser(%s, %s, %s, %s)'
        cursor.execute(sql, (username, email, password, fullname))
        connection.commit()
        cursor.close()
    # Devolver un mensaje de éxito
        return jsonify({'message': 'Usuario registrado correctamente'}), 201

# Ruta para cambiar contraseña


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


# Ruta para actualizar un nuevo usuario en la base de datos
# @main.route('/register/<id>', methods=['PUT'])
# def update_user(id):
#     # has_access = Security.verify_token(request.headers)

#     # if has_access:
#     # if validate_id(id) and (request.json["nombre"]):
#     try:
#         user = UserService.get_user_by_id(id)
#         if user != None:
#             try:
#                 username = request.json["username"]
#                 email = request.json["email"]
#                 password = request.json["password"]
#                 fullname = request.json["fullname"]

#                 user = User(id, username, email, password, fullname, None)

#                 updated_user = UserService.update_user(id, user)

#                 return jsonify({"message": 'User updated successfully', "success": True}), 201
#             except Exception as ex:
#                 Logger.add_to_log("error132", str(ex))
#                 Logger.add_to_log("error133", traceback.format_exc())
#         else:
#             return jsonify({"message": "user not found", "success": False})
#     except Exception as ex:
#         Logger.add_to_log("error137", str(ex))
#         Logger.add_to_log("error138", traceback.format_exc())
    # else:
    #     return jsonify({"message": "Invalid parameters...", "success": False})
    # else:
    #     response = jsonify({'message': 'Unauthorized'})


# Ruta para iniciar sesión con un usuario y obtener un token JWT

@main.route('/login', methods=['POST'])
def login():
    # Obtener los datos del usuario del cuerpo de la solicitud
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Validar que los datos no estén vacíos
    if not username or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    # Autenticar al usuario con su correo electrónico y contraseña y generar un token JWT
    token = authenticate(username, password)
    # Si el token es válido, devolverlo al usuario
    if token:
        return jsonify({'token': token}), 200
    # Si no, devolver un mensaje de error
    else:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 202


# Ruta para obtener el perfil del usuario a partir de un token JWT

@main.route('/profile', methods=['GET'])
def profile():
    # Obtener el token JWT de la cabecera de la solicitud
    auth_header = request.headers.get('Authorization')
    # Validar que el token exista y tenga el formato correcto
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Falta el token'}), 401
    token = auth_header.split()[1]
    # Verificar el token JWT y obtener la información del usuario
    user = verify_token(token)
    # Si el usuario es válido, devolver su información
    if user:
        return jsonify(user), 200
    # Si no, devolver un mensaje de error
    else:
        return jsonify({'message': 'Token inválido o expirado, inicia sesión para continuar.'}), 401
