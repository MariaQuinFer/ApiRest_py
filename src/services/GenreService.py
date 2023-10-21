# Models
from src.models.GenreModel import Genre


class GenreService():

    @staticmethod
    def list_genres():
        return Genre.list_genres()

    @staticmethod
    def get_genres_by_id(id):
        return Genre.get_genre_by_id(id)

    @staticmethod
    def add_genre(genre):
        genre = Genre(id, name=genre.name)
        genre.add_genre(genre)

    @staticmethod
    def delete_genre(id):
        return Genre.delete_genre(id)

    @staticmethod
    def update_genre(id, genre):
        genre = Genre(id, name=genre.name)
        return Genre.update_genre(id, genre)
