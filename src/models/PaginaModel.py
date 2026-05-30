import mysql.connector
from models.Database import Database

class PaginaModel:
    def __init__(self, db: Database):
        self.db = db
    
    def data(self, email_usuario = None, id = None):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True) # type: ignore
            
            query = "SELECT * FROM paginas WHERE "
            params = []
            if email_usuario:
                query += "email_usuario = %s"
                params.append(email_usuario)
            elif id:
                query += "id = %s"
                params.append(id)
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall() if email_usuario else cursor.fetchone()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        finally:
            cursor.close()
            conn.close() # type: ignore
    
    def crear(self, email_usuario, titulo = "Sin Titulo", contenido = ""):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor() # type: ignore

            cursor.execute(
                """INSERT INTO paginas (email_usuario, titulo, contenido)
                VALUES (%s, %s, %s)""",
                (email_usuario, titulo, contenido)
            )

            conn.commit() # type: ignore
            return True, ""

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar crear la pagina, prueba de nuevo"

        finally:
            cursor.close()
            conn.close() # type: ignore


    def editar(self, id, titulo = "Sin Titulo", contenido = ""):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor() # type: ignore

            cursor.execute("UPDATE paginas SET titulo = %s, contenido = %s WHERE id = %s", (titulo, contenido, id))
            conn.commit() # type: ignore
            return True, ""

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar editar la pagina, prueba de nuevo"

        finally:
            cursor.close()
            conn.close() # type: ignore


    def eliminar(self, email_usuario = None, id = None):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor() # type: ignore
            
            query = "DELETE FROM paginas WHERE "
            params = []
            if email_usuario:
                query += "email_usuario = %s"
                params.append(email_usuario)
                
            elif id:
                query += "id = %s"
                params.append(id)
            
            cursor.execute(query, tuple(params))
            return conn.commit() # type: ignore

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        finally:
            cursor.close()
            conn.close() # type: ignore
