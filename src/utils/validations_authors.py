# Validate the author's name (if it is a text between 1 and 255 characters).
def validate_name(nombre: str) -> bool:
    return (len(nombre) > 0 and len(nombre) <= 255)


def validate_id(id: str) -> bool:
    return (id.isnumeric())
