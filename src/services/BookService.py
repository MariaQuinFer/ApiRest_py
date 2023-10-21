# Models
from src.models.BookModel import Book


class BookService():

    @staticmethod
    def list_books():
        return Book.list_books()

    @staticmethod
    def read_booK_by_id(ISBN):
        return Book.read_booK_by_id(ISBN)

    @staticmethod
    def create_book(book):
        book = Book(id, ISBN=book.ISBN, titulo=book.titulo, idAutor=book.idAutor, idGenre=book.idGenre, idEditorial=book.idEditorial,
                    idioma=book.idioma, paginas=book.paginas, portada=book.portada, descripcion=book.descripcion, estado=book.estado)
        book.add_book(book)

    @staticmethod
    def delete_book(ISBN):
        return Book.delete_book(ISBN)

    @staticmethod
    def update_book(ISBN, book):
        book = Book(id, ISBN, titulo=book.titulo, idAutor=book.idAutor, idGenre=book.idGenre, idEditorial=book.idEditorial,
                    idioma=book.idioma, paginas=book.paginas, portada=book.portada, descripcion=book.descripcion, estado=book.estado)
        return Book.update_book(ISBN, book)
