# Models
from src.models.AuthorModel import Author


class AuthorService():

    @staticmethod
    def list_authors():
        return Author.list_authors()

    @staticmethod
    def get_author_by_id(id):
        return Author.get_author_by_id(id)

    @staticmethod
    def add_author(author):
        author = Author(id, nombre=author.nombre)
        author.add_author(author)

    @staticmethod
    def delete_author(id):
        return Author.delete_author(id)

    @staticmethod
    def update_author(id, author):
        author = Author(id, nombre=author.nombre)
        return Author.update_author(id, author)
