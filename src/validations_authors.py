# Valida el nombre del autor (si es un texto de entre 1 y 255 caracteres).
def validate_name(nombre: str) -> bool:
    return (len(nombre) > 0 and len(nombre) <= 255)


def validate_id(id: str) -> bool:
    return (id.isnumeric())
