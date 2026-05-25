import mysql.connector
from models.Database import Database

class PaginaModel:
    def __init__(self, db: Database):
        self.db = db
    
    def data(self, email):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True) # type: ignore

            cursor.execute(
                """
                SELECT * FROM paginas WHERE email_usuario = %s
                """,
                (email,)
            )

            return cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        finally:
            cursor.close()
            conn.close()
    
    def crear(self, email, titulo, contenido):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO paginas (email_usuario, titulo, contenido)
                VALUES (%s, %s, %s)
                """,
                (email, titulo, contenido)
            )

            conn.commit()
            return True, "Página creada correctamente"

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al crear"

        finally:
            cursor.close()
            conn.close()


    def editar(self, id_pagina, nombre, contenido):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE paginas
                SET nombre = %s,
                    contenido = %s
                WHERE id = %s
                """,
                (nombre, contenido, id_pagina)
            )

            conn.commit()
            return True, "Actualizada correctamente"

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al editar"

        finally:
            cursor.close()
            conn.close()


    def eliminar(self, id_pagina):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM paginas WHERE id = %s",
                (id_pagina,)
            )

            conn.commit()
            return True, "Eliminada correctamente"

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al eliminar"

        finally:
            cursor.close()
            conn.close()
