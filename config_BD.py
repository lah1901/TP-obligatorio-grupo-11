"""
Este módulo contiene la configuración y la función para la conexión a la base de datos.
"""

import mysql.connector
from mysql.connector import Error

def connectionBD():
    """
    Establece una conexión con la base de datos.

    Returns:
        mydb (mysql.connector.connection_cext.CMySQLConnection): La conexión a la base de datos si es exitosa.
        None: Si ocurre un error en la conexión.
    """
    try:
        # Intentar establecer la conexión a la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="usuariosgamers"
        )
        print("Conexión exitosa")
        return mydb
    except Error as err:
        # Manejar cualquier error que ocurra durante la conexión
        print(f"Error en la conexión a la base de datos: {err}")
        return None

if __name__ == "__main__":
    connectionBD()
