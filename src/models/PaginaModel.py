import mysql.connector
from models.Database import Database

class PaginaModel:
    def __init__(self, db: Database):
        self.db = db
    
    def data(self, email_usuario, id = None):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True) # type: ignore
            
            query = "SELECT * FROM paginas WHERE email_usuario = %s"
            params = [email_usuario]
            if id:
                query += " AND id = %s"
                params.append(id)
            
            cursor.execute(query, tuple(params))
            return cursor.fetchone() if id else cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        finally:
            cursor.close()
            conn.close()
    
    def crear(self, email_usuario, titulo = "Sin Titulo", contenido = ""):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO paginas (email_usuario, titulo, contenido)
                VALUES (%s, %s, %s)""",
                (email_usuario, titulo, contenido)
            )

            conn.commit()
            return True, ""

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar crear la pagina, prueba de nuevo"

        finally:
            cursor.close()
            conn.close()


    def editar(self, id, titulo = "Sin Titulo", contenido = ""):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE paginas SET titulo = %s, contenido = %s WHERE id = %s", (titulo, contenido, id))
            conn.commit()
            return True, ""

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar editar la pagina, prueba de nuevo"

        finally:
            cursor.close()
            conn.close()


    def eliminar(self, id):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM paginas WHERE id = %s", (id,))
            conn.commit()
            return True, ""

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar eliminar la pagina, prueba de nuevo"

        finally:
            cursor.close()
            conn.close()
