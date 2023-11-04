# Services
from src.services.AuthorService import AuthorService


def test_list_authors_not_none():
    authors = AuthorService.list_authors()
    assert authors != None


def test_get_auhtors_has_elements():
    authors = AuthorService.list_authors()
    assert len(authors) > 0


def test_get_authors_check_elements_length():
    authors = AuthorService.list_authors()
    for author in authors:
        assert len(author) > 0
