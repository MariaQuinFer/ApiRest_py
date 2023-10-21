# from decouple import config
# import datetime
# import jwt
# import pytz

# from src.database.db import get_connection


# class AuthenticateServices():
#     # secret = config('JWT_KEY')
#     # tz = pytz.timezone("Europe/Madrid")

#     @classmethod
#     def authenticate(username, password):
#         # Buscar al usuario por su correo electrónico en la base de datos
#         connection = get_connection()
#         with connection.cursor() as cursor:
#             sql = "call sp_verifyLogin(%s, %s)"
#             cursor.execute(sql, (username, password))
#             user = cursor.fetchone()
#             cursor.close()
#         # Si el usuario existe y la contraseña coincide, generar un token JWT con su información y una fecha de expiración
#         if user and user[3] == password:
#             token = jwt.encode({
#                 'id': user[0],
#                 'username': user[1],
#                 'email': user[2],
#                 'iat': datetime.datetime.utcnow(),
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
#             }, config('JWT_KEY'), algorithm="HS256")
#             return token
#         # Si no, devolver None
#         else:
#             return None

#     @classmethod
#     def verify_token(token):
#         # Intentar decodificar el token JWT con el secreto de la aplicación
#         try:
#             data = jwt.decode(
#                 token, config('JWT_KEY'), algorithms=["HS256"])
#             # Buscar al usuario por su id en la base de datos
#             connection = get_connection()
#             with connection.cursor() as cursor:
#                 sql = "SELECT id, username, email FROM users WHERE id = %s"
#                 cursor.execute(sql, (data['id'],))
#                 user = cursor.fetchone()
#                 cursor.close()
#             # Si el usuario existe, devolver su información
#             if user:
#                 return {
#                     'id': user[0],
#                     'username': user[1],
#                     'email': user[2]
#                 }
#             # Si no, devolver None
#             else:
#                 return None
#         # Si ocurre algún error al decodificar el token JWT, devolver None
#         except Exception as e:
#             return None
