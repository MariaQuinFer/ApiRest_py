# Model
from src.models.LendModel import Lend


class LendService():
    @staticmethod
    def lend_book(lend):
        lend = Lend(id, idUser=lend.idUser, ISBN=lend.ISBN,
                    departury_date=lend.departury_date, return_date=lend.return_date, action=lend.action)
        lend.lend_book(lend)

    @staticmethod
    def delete_lend(id):
        return Lend.delete_lend(id)

    @staticmethod
    def update_action(id, lend):
        lend = Lend(id=lend.id, idUser=lend.idUser, ISBN=lend.ISBN,
                    departury_date=lend.departury_date, return_date=lend.return_date, action=lend.action)
        return Lend.update_action(id, lend)
