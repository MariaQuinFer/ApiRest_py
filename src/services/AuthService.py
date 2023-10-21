# import traceback

# # Database
# from src.database.db import get_connection
# # Errors
# from src.utils.errors.CustomException import CustomException
# # Logger
# from src.utils.Logger import Logger
# # Models
# from src.models.UserModel import User

# import jwt


# class AuthService():

#     @staticmethod
#     def list_user():
#         try:
#             connection = get_connection()
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                 SELECT *
#                 FROM user
#                 """)
#                 data = cursor.fetchall()
#                 print(data)
#             return [User.from_row(row) for row in data]
#         except Exception as ex:
#             Logger.add_to_log("error", str(ex))
#             Logger.add_to_log("error", traceback.format_exc())

# @staticmethod
# def verify_username_email(user):
#     try:
#         connection = get_connection()
#         verify_user = None
#         with connection.cursor() as cursor:
#             cursor.execute('call sp_verifyData(%s, %s)',
#                            (user.username, user.email))
#             row = cursor.fetchone()
#             # print("row:", row)
#             if row != None:
#                 verify_user = User(
#                     int(row[0]), row[1], row[2], None, None, None)
#         connection.close()
#         print("Verify:", verify_user)
#         return verify_user
#     except Exception as ex:
#         Logger.add_to_log("error", str(ex))
#         Logger.add_to_log("error", traceback.format_exc())

# @staticmethod
# def register_user(user):
#     try:
#         connection = get_connection()
#         registered_user = None
#         with connection.cursor() as cursor:
#             cursor.execute('call sp_addUser(%s, %s, %s, %s)',
#                            (user.username, user.email, user.password, user.fullname))
#             connection.commit()
#         connection.close
#         return registered_user
#     except Exception as ex:
#         Logger.add_to_log("error", str(ex))
#         Logger.add_to_log("error", traceback.format_exc())

#         # try:
#         #     connection = get_connection()
#         #     registered_user = None
#         #     with connection.cursor() as cursor:
#         #         cursor.execute("""
#         #         INSERT INTO users (username, email, password, fullname, usertype)
#         #         VALUES('{0}','{1}','{2}','{3}','{4}')
#         #         """, (user.username, user.email, user.password, user.fullname, user.usertype))
#         #         connection.commit()
#         #     connection.close()
#         #     print(user.username)
#         #     return registered_user
#         # except CustomException as ex:
#         #     raise CustomException(ex)

#     @classmethod
#     def login_user(cls, user):
#         try:
#             connection = get_connection()
#             authenticated_user = None
#             with connection.cursor() as cursor:
#                 cursor.execute('call sp_verifyIdentity(%s, %s)',
#                                (user.username, user.password))
#                 row = cursor.fetchone()
#                 print("row:", row)
#                 if row != None:
#                     authenticated_user = User(
#                         int(row[0]), row[1], None, None, row[2], None)
#             connection.close()
#             print("Ath:", authenticated_user)
#             return authenticated_user
#         except Exception as ex:
#             Logger.add_to_log("error", str(ex))
#             Logger.add_to_log("error", traceback.format_exc())

#     @classmethod
#     # Función para verificar el token JWT del usuario y obtener su información
#     def user(id):
#         # Intentar decodificar el token JWT con el secreto de la aplicación
#         try:
#             connection = get_connection()
#             with connection.cursor() as cursor:
#                 sql = "SELECT id, name, email FROM users WHERE id = %s".format(
#                     id)
#                 cursor.execute(sql)
#                 user = cursor.fetchone()
#             # Si el usuario existe, devolver su información

#                 if user != None:
#                     verify_user = User.from_row(user)
#             connection.close()
#             return verify_user
#         # Si ocurre algún error al decodificar el token JWT, devolver None
#         except Exception as ex:
#             Logger.add_to_log("error", str(ex))
#             Logger.add_to_log("error", traceback.format_exc())
