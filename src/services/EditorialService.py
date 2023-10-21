# Models
from src.models.EditorialModel import Editorial


class EditorialService():

    @staticmethod
    def list_editorials():
        return Editorial.list_editorials()

    @staticmethod
    def get_editorial_by_id(id):
        return Editorial.get_editorial_by_id(id)

    @staticmethod
    def add_editorial(editorial):
        editorial = Editorial(id, name=editorial.name)
        editorial.add_editorial(editorial)

    @staticmethod
    def delete_editorial(id):
        return Editorial.delete_editorial(id)

    @staticmethod
    def update_editorial(id, editorial):
        editorial = Editorial(id, name=editorial.name)
        return Editorial.update_editorial(id, editorial)
