from decouple import config
import datetime
import jwt
import pytz


class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("Europe/Madrid")

    # @classmethod
    # def generate_token(cls, authenticated_user):
    #     payload = {
    #         'iat': datetime.datetime.now(tz=cls.tz),
    #         'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=100),
    #         'username': authenticated_user.username,
    #         'fullname': authenticated_user.fullname,
    #         'roles': ['Administrator', 'User']
    #     }
    #     return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            # print("auth", authorization)
            encoded_token = authorization.split(" ")[1]
            # print("token", encoded_token)

            # if (len(encoded_token) > 0):
            try:
                payload = jwt.decode(
                    encoded_token, cls.secret, algorithms=["HS256"])
                # print(payload)

                return True
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False
        return False

    # @classmethod
    # def extract_user(cls, headers):
    #     if 'Authorization' in headers.keys():
    #         authorization = headers['Authorization']
    #         print("auth", authorization)
    #         encoded_token = authorization.split(" ")[1]
    #         print("token", encoded_token)

    #         # if (len(encoded_token) > 0):
    #         try:
    #             payload = jwt.decode(
    #                 encoded_token, cls.secret, algorithms=["HS256"])
    #             print(payload)

    #             username = (payload['username'])
    #             print(username)
    #             return username
    #         except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
    #             return None
    #     return None
