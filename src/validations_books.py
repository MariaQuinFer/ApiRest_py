# Valida el ISBN (si es un texto sin espacios en blanco de entre 1 y 30 caracteres).
def validate_ISBN(ISBN: str) -> bool:
    ISBN = ISBN.strip()
    return (len(ISBN) > 0 and len(ISBN) <= 13)

# Valida el titulo (si es un texto de entre 1 y 255 caracteres).


def validate_title(titulo: str) -> bool:
    return (len(titulo) > 0 and len(titulo) <= 255)

# Valida que la idAutor sea un número.


def validate_idAuthor(idAutor: str) -> bool:
    idAutor = str(idAutor)
    if idAutor.isnumeric():
        return (int(idAutor) >= 1)
    else:
        return False

# Valida que la idGenre sea un número.


def validate_idGenre(idGenre: str) -> bool:
    idGenre = str(idGenre)
    if idGenre.isnumeric():
        return (int(idGenre) >= 1)
    else:
        return False

# Valida que la idEditorial sea un número.


def validate_idEditorial(idEditorial: str) -> bool:
    idEditorial = str(idEditorial)
    if idEditorial.isnumeric():
        return (int(idEditorial) >= 1)
    else:
        return False

# Valida el titulo (si es un texto de entre 1 y 255 caracteres).


def validate_title(titulo: str) -> bool:
    return (len(titulo) > 0 and len(titulo) <= 255)

# Valida el idioma (si es un texto de entre 1 y 45 caracteres).


def validate_language(idioma: str) -> bool:
    return (len(idioma) > 0 and len(idioma) <= 255)

# Valida que páginas sea un número.


def validate_pages(paginas: str) -> bool:
    paginas = str(paginas)
    if paginas.isnumeric():
        return (int(paginas) >= 1)
    else:
        return False

# Valida la portada (si es un texto de entre 1 y 255 caracteres).


def validate_cover(portada: str) -> bool:
    return (len(portada) > 0 and len(portada) <= 255)

# Valida la descripcion (si es un texto de entre 1 y 2000 caracteres).


def validate_description(descripcion: str) -> bool:
    return (len(descripcion) > 0 and len(descripcion) <= 2000)
