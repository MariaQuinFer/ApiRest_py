# Validate the ISBN (if it is text without whitespace between 1 and 30 characters).
def validate_ISBN(ISBN: str) -> bool:
    ISBN = ISBN.strip()
    return (len(ISBN) > 0 and len(ISBN) <= 13)


# Validate the title (if it is a text between 1 and 255 characters).


def validate_title(titulo: str) -> bool:
    return (len(titulo) > 0 and len(titulo) <= 255)

# Validates that the idAuthor is a number.


def validate_idAuthor(idAutor: str) -> bool:
    idAutor = str(idAutor)
    if idAutor.isnumeric():
        return (int(idAutor) >= 1)
    else:
        return False

# Validates that the idGenre is a number.


def validate_idGenre(idGenre: str) -> bool:
    idGenre = str(idGenre)
    if idGenre.isnumeric():
        return (int(idGenre) >= 1)
    else:
        return False

# Validates that the idEditorial is a number.


def validate_idEditorial(idEditorial: str) -> bool:
    idEditorial = str(idEditorial)
    if idEditorial.isnumeric():
        return (int(idEditorial) >= 1)
    else:
        return False

# Validate the title (if it is a text between 1 and 255 characters).


def validate_title(titulo: str) -> bool:
    return (len(titulo) > 0 and len(titulo) <= 255)

# Validate the language (if it is a text between 1 and 45 characters).


def validate_language(idioma: str) -> bool:
    return (len(idioma) > 0 and len(idioma) <= 255)

# Validate that pages is a number.


def validate_pages(paginas: str) -> bool:
    paginas = str(paginas)
    if paginas.isnumeric():
        return (int(paginas) >= 1)
    else:
        return False

# Validate the url_cover (if it is text between 1 and 255 characters).


def validate_cover(portada: str) -> bool:
    return (len(portada) > 0 and len(portada) <= 255)


# Validate the description (if it is a text between 1 and 2000 characters).

def validate_description(descripcion: str) -> bool:
    return (len(descripcion) > 0 and len(descripcion) <= 2000)
