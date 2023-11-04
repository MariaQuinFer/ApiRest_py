from decouple import config
import jwt


class Security():

    secret = config('JWT_KEY')

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            try:
                payload = jwt.decode(
                    encoded_token, cls.secret, algorithms=["HS256"])

                return True
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False
        return False
