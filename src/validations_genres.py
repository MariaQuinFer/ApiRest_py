# Valida elnombre del género (si es un texto de entre 1 y 255 caracteres).
def validate_name(name: str) -> bool:
    return (len(name) > 0 and len(name) <= 255)


def validate_id(id: str) -> bool:
    return (id.isnumeric())
