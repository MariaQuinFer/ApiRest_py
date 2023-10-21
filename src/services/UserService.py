# Model
from src.models.UserModel import User


class UserService():

    @staticmethod
    def list_users():
        return User.list_users()

    @staticmethod
    def get_user_by_id(id):
        return User.get_user_by_id(id)

    @staticmethod
    def delete_user(id):
        return User.delete_user(id)

    @staticmethod
    def update_usertype(id, user):
        user = User(id, username=user.username, email=user.email,
                    password=user.password, fullname=user.fullname, usertype=user.usertype)
        return User.update_usertype(id, user)

    def update_password(id, user):
        user = User(id, username=user.username, email=user.email,
                    password=user.password, fullname=user.fullname, usertype=user.usertype)
        return User.update_password(id, user)

    # @staticmethod
    # def verify_username(user):
    #     user = User(id, username=user.username, email=user.email,
    #                 password=user.password, fullname=user.fullname, usertype=user.usertype)
    #     return User.verify_username(user)

    # @staticmethod
    # def verify_email(user):
    #     user = User(id, username=user.username, email=user.email,
    #                 password=user.password, fullname=user.fullname, usertype=user.usertype)
    #     return User.verify_email(user)

    # @staticmethod
    # def register_user(user):
    #     user = User(id, username=user.username, email=user.email,
    #                 password=user.password, fullname=user.fullname, usertype=user.usertype)
    #     return User.register_user(user)

    # @staticmethod
    # def update_user(id, user):
    #     user = User(id, username=user.username, email=user.email,
    #                 password=user.password, fullname=user.fullname, usertype=user.usertype)
    #     return User.update_user(id, user)
