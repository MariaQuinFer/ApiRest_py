# Database
from src.database.db import get_connection


class Book():

    def __init__(self, id, ISBN, titulo, idAutor, idGenre, idEditorial, idioma, paginas, portada, descripcion, estado) -> None:
        self.id = id
        self.ISBN = ISBN
        self.titulo = titulo
        self.idAutor = idAutor
        self.idGenre = idGenre
        self.idEditorial = idEditorial
        self.idioma = idioma
        self.paginas = paginas
        self.portada = portada
        self.descripcion = descripcion
        self.estado = estado

    def to_json(self):
        return {
            'id': self.id,
            'ISBN': self.ISBN,
            'titulo': self.titulo,
            'idAutor': self.idAutor,
            'idGenre': self.idGenre,
            'idEditorial': self.idEditorial,
            'idioma': self.idioma,
            'paginas': self.paginas,
            'portada': self.portada,
            'descripcion': self.descripcion,
            'estado': self.estado,
        }

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])

    @staticmethod
    def list_books():
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT l.id, l.ISBN, l.titulo, a.nombre AS autor, g.name AS genero, e.name AS editorial, l.idioma, l.paginas, l.portada, l.descripcion, l.estado
            FROM libros l 
            JOIN autores a 
            ON l.idAutor=a.id 
            JOIN genres g 
            ON l.idGenre=g.id 
            JOIN editorials e 
            ON l.idEditorial=e.id ORDER BY l.idAutor ASC;
            """)
            data = cursor.fetchall()  # trae todos los datos
            return [Book.from_row(row) for row in data]

    @staticmethod
    def read_booK_by_id(ISBN):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT l.id, l.ISBN, l.titulo, a.nombre AS autor, g.name AS genero, e.name AS editorial, l.idioma, l.paginas, l.portada, l.descripcion, l.estado
                FROM libros l 
                JOIN autores a 
                ON l.idAutor=a.id 
                JOIN genres g 
                ON l.idGenre=g.id 
                JOIN editorials e 
                ON l.idEditorial=e.id 
                WHERE l.ISBN = '{0}'
            """.format(ISBN)
            cursor.execute(sql)

            data = cursor.fetchone()
            if data != None:
                return Book.from_row(data)
            else:
                return None

    @staticmethod
    def add_book(book):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
        INSERT INTO libros (ISBN, titulo, idAutor, idGenre, idEditorial, idioma, paginas, portada, descripcion, estado)
        VALUES ('{0}', '{1}', {2}, {3}, {4}, '{5}', {6}, '{7}', '{8}', '{9}')
        """.format(book.ISBN, book.titulo, book.idAutor, book.idGenre, book.idEditorial,
                   book.idioma, book.paginas, book.portada, book.descripcion, book.estado)
        cursor.execute(sql)
        connection.commit()  # Confirma la accion de añadir libro

    @staticmethod
    def delete_book(ISBN):
        connection = get_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM libros WHERE ISBN='{0}'".format(ISBN)
        cursor.execute(sql)
        connection.commit()  # Confirma que se ha eliminado un libro

    @staticmethod
    def update_book(ISBN, book):
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE libros 
            SET titulo = '{1}', 
                idAutor = {2}, 
                idGenre = {3} , 
                idEditorial = {4}, 
                idioma = '{5}', 
                paginas = {6}, 
                portada = '{7}', 
                descripcion = '{8}', 
                estado='{9}'
            WHERE ISBN = '{0}'
        """.format(ISBN, book.titulo, book.idAutor, book.idGenre, book.idEditorial,
                   book.idioma, book.paginas, book.portada, book.descripcion, book.estado)
        cursor.execute(sql)
        connection.commit()  # Confirma la accion de modificar un libro
