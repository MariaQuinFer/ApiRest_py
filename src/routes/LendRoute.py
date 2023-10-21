from flask import Blueprint, request, jsonify
import traceback

from src.database.db import get_connection

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.LendService import LendService
# Model
from src.models.LendModel import Lend
# DataBase
from src.database.db import get_connection


lend = Blueprint("lend", __name__)


def update_book_status(ISBN):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Ejecutar el código SQL para actualizar el estado del libro
        sql = ("""
            UPDATE libros
            SET estado = "No disponible"
            WHERE ISBN = '{0}'
        """.format(ISBN))
        cursor.execute(sql)
    # Confirmar los cambios en la base de datos
    connection.commit()
    # Cerrar el cursor
    cursor.close()


def update_book_status_again(ISBN):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Ejecutar el código SQL para actualizar el estado del libro
        sql = ("""
            UPDATE libros
            SET estado = "Disponible"
            WHERE ISBN = '{0}'
        """.format(ISBN))
        cursor.execute(sql)
    # Confirmar los cambios en la base de datos
    connection.commit()
    # Cerrar el cursor
    cursor.close()


# Ruta para solicitar un préstamo:
@lend.route("/lend", methods=['POST'])
def lend_book():

    has_access = Security.verify_token(request.headers)

    if has_access:

        try:
            idUser = request.json["idUser"]
            ISBN = request.json["ISBN"]

            lend = Lend(id, idUser, ISBN, None, None, None)
            created_loan = LendService.lend_book(lend)

            return jsonify({"message": 'Loan created successfully', "success": True}), 201
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

# Ruta para eliminar un préstamo


@lend.route("/lend/<id>", methods=["DELETE"])
def delete_lend(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            LendService.delete_lend(id)
            return jsonify({"message": "Loan deleted", "success": True}), 204
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

# Ruta para actualizar el estado del préstamo (prestado o devuelto)


@lend.route("/lend/<id>", methods=['PUT'])
def update_action(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            action = request.json["action"]
            loan = Lend(id, None, None, None, None, action)

            updated_loan = LendService.update_action(
                id, loan)

            return jsonify({"message": 'Loan updated successfully', "success": True}), 201
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

# Ruta para obetner una lista con todos los préstamos(devoluciones) realizados


@lend.route("/lend", methods=['GET'])
def lend_list():

    has_access = Security.verify_token(request.headers)

    if has_access:

        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = """
                    SELECT p.id, u.fullname, p.ISBN, l.titulo, a.nombre, departury_date, p.return_date, p.action
                    FROM prestamo p
                    JOIN users u
                    ON p.idUSer = u.id
                    JOIN libros l
                    ON p.ISBN = l.ISBN 
                    JOIN autores a
                    ON l.idAutor = a.id  
                    ORDER BY action DESC;
                """
            cursor.execute(sql)
            data = cursor.fetchall()

            if data != None:
                loans = []
                # print("data", data)
                for row in data:
                    loan = {
                        "id": row[0],
                        "fullname": row[1],
                        "ISBN": row[2],
                        "titulo": row[3],
                        "autor": row[4],
                        "departury_date": row[5],
                        "return_date": row[6],
                        "action": row[7],
                    }
                    loans.append(loan)
                return jsonify({"Loans": loans, "message": 'Lista de préstamos', "success": True}), 200
            else:
                return jsonify({"mesagge": "Not found", "success": False}), 205
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


# Ruta para obtener el usuario con sesion iniciada junto con el libro prestado si tiene préstamo

@lend.route("/lend/<id>", methods=['GET'])
def lend_user_book(id):

    has_access = Security.verify_token(request.headers)

    if has_access:

        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = """
                    SELECT u.username, u.email, u.password, u.fullname, p.ISBN, p.return_date, p.action, l.titulo, a.nombre
                    FROM users u
                    JOIN prestamo p
                    ON u.id = p.idUSer
                    JOIN libros l
                    ON p.ISBN = l.ISBN
                    JOIN autores a
                    ON l.idAutor= a.id
                    WHERE u.id= {0} AND
                    action="Prestado"
                    ORDER BY return_date                 
                """.format(id)
            # print(nombre)
            cursor.execute(sql)
            data = cursor.fetchone()

            if data != None:
                # print("data", data)
                user = {
                    "username": data[0],
                    "email": data[1],
                    "password": data[2],
                    "fullname": data[3],
                    "ISBN": data[4],
                    "return_date": data[5],
                    "action": data[6],
                    "titulo": data[7],
                    "nombre": data[8],
                }
                return jsonify({"user": user, "message": 'Usuario actual', "success": True}), 200
            else:
                return jsonify({"mesagge": "Usuario sin préstamo actualmente", "success": False}), 205
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
