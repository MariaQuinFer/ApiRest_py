# from src.models.UserModel import User
# from src.services.AuthService import AuthService
# from src.utils.Security import Security

# from flask import Blueprint, request, jsonify

# import traceback

# # from flask_login import login_user, logout_user, login_required

# # Errors
# from src.utils.errors.CustomException import CustomException

# # Logger
# from src.utils.Logger import Logger

# # Security
# # Services
# # Model


# main = Blueprint("authorization", __name__)


# @main.route("/register", methods=['GET', 'POST'])
# def register():
#     # has_access = Security.verify_token(request.headers)

#     # if has_access:

#     if request.method == 'GET':
#         try:
#             users = AuthService.list_user()
#             print("Objeto:", users)
#             if (len(users) > 0):
#                 print(len(users))
#                 users = [user.__dict__ for user in users]
#                 return jsonify({'users': users, 'message': "user list",  'sucess': True})
#             else:
#                 return jsonify({'message': "Not found", 'success': True})
#         except Exception as ex:
#             Logger.add_to_log("error", str(ex))
#             Logger.add_to_log("error", traceback.format_exc())

#     if request.method == 'POST':
#         try:
#             username = request.json['username']
#             email = request.json['email']
#             print(username)
#             print(email)
#             user = User(0, username, email, None, None, None)
#             verify_user = AuthService.verify_username_email(user)
#             print(verify_user)

#             if verify_user:
#                 return jsonify({"message": "Username already exits, cannot be duplicated", "Success": False})
#             else:

#                 try:
#                     username = request.json['username']
#                     email = request.json['email']
#                     password = request.json['password']
#                     fullname = request.json['fullname']

#                     user = User(0, username, email, password,
#                                 fullname, usertype="user")

#                     AuthService.register_user(user)
#                     return jsonify({"message": "Add user", "success": True})
#                 except Exception as ex:
#                     Logger.add_to_log("error", str(ex))
#                     Logger.add_to_log("error", traceback.format_exc())
#         except Exception as ex:
#             Logger.add_to_log("error", str(ex))
#             Logger.add_to_log("error", traceback.format_exc())

# else:
#     response = jsonify({'message': 'Unauthorized'})
#     return response, 401


# @main.route('/login', methods=['POST'])
# def login():
#     username = request.json['username']
#     password = request.json['password']
#     # print(username, password)

#     _user = User(0, username, None, password, None, None)
#     # print("_user", _user)
#     authenticated_user = AuthService.login_user(_user)
#     # print("user:", authenticated_user)

#     if (authenticated_user != None):
#         # login_user(_user)

#         encoded_token = Security.generate_token(authenticated_user)
#         return jsonify({'status': "created", 'success': True, 'username': username, 'token': encoded_token})
#     else:
#         return jsonify({'status': 'Unauthorized'})


# @main.route('/profile', methods=['GET'])
# def profile():

#     has_access = Security.verify_token(request.headers)

#     Logger.add_to_log("ERRORRR", str(request.headers))

#     if has_access:
#         user = Security.extract_user(request.headers)
#         print("usuario:", user)
#         if user:
#             return jsonify(user), 200
#     # Si no, devolver un mensaje de error
#         else:
#             return jsonify({'message': 'Token inválido o expirado'}), 401
#         # else:
#     #     response = jsonify({'message': 'Unauthorized'})
#     #     return response, 401
