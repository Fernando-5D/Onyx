import bcrypt
import mysql.connector
from models.Database import Database

class UsuarioModel:
    def __init__(self, db: Database):
        self.db = db
        
    def actualizar_passw(self, email, nueva_passw):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            hashed_passw = bcrypt.hashpw(nueva_passw.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

            sql = """ UPDATE usuarios SET passw = %s WHERE email = %s """
            cursor.execute(sql,(hashed_passw, email))
            conn.commit()
            return True, "Contraseña actualizada"

        except Exception as e:
            print(e)
            return False, "Error actualizando contraseña"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    
    def iniciar_sesion(self, email, passw):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True) # type: ignore
            cursor.execute("SELECT passw FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                if bcrypt.checkpw(passw.encode('utf-8'), user['passw'].encode('utf-8')):
                    return True, ""
                else:
                    return False, "La contraseña es incorrecta"
            else:
                return False, "No se encontró una cuenta con ese correo electrónico"
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar iniciar sesión"
        
        finally:
            cursor.close()
            conn.close() # type: ignore
    
    def registrar(self, nombre, email, passw):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor() # type: ignore
            
            hashed_passw = bcrypt.hashpw(passw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cursor.execute(
                """INSERT INTO usuarios (nombre, email, passw)
                VALUES (%s, %s, %s)""", (nombre, email, hashed_passw)
            )
            
            conn.commit() # type: ignore
            return True, ""
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar registrarte"
        
        finally:
            cursor.close()
            conn.close() # type: ignore
    
    def eliminar(self, email):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor() # type: ignore
            
            cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
            conn.commit() # type: ignore
            return True, ""
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, "Hubo un error al intentar eliminar tu cuenta"
        
        finally:
            cursor.close()
            conn.close() # type: ignore
    
    def data(self, email, campo = "*"):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True) # type: ignore
            
            cursor.execute(f"SELECT {campo} FROM usuarios WHERE email = %s", (email,))
            return cursor.fetchone() # type: ignore
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
        finally:
            cursor.close()
            conn.close() # type: ignore
        