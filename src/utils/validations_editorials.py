# Validates the name of the publisher (if it is a text between 1 and 255 characters).
def validate_name(name: str) -> bool:
    return (len(name) > 0 and len(name) <= 255)


def validate_id(id: str) -> bool:
    return (id.isnumeric())
