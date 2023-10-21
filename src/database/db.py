# from flask_mysqldb import MySQL
from decouple import config
import pymysql
import traceback


from src.utils.Logger import Logger


# from app import app

# Connection DB
# conexion = MySQL(app)


def get_connection():
    try:
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB')
        )
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
