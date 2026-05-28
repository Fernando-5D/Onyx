from pydantic import ValidationError
from models.EmailSender import EmailSender
from models.UsuarioModel import UsuarioModel
from models.Database import Database
from models.schemas import UsuarioSesion_Schema, UsuarioRegistro_Schema, UsuarioBase_Schema, UsuarioRecuperarPassw_Schema

class UsuarioCtrl:
    def __init__(self):
        self.model = UsuarioModel(Database())
    
    def obtener_data(self, email, campo):
        return self.model.data(email, campo)
    
    def iniciar_sesion(self, email, passw):
        try:
            data = UsuarioSesion_Schema(email=email, passw=passw)
            is_valid, mensaje = self.model.iniciar_sesion(data.email, data.passw)
            return is_valid, mensaje
            
        except ValidationError as err:
            print(f"Error de validación: {err}")
            if "email" in err.errors()[0]['loc']:
                return False, "El correo electrónico no es válido"
            
            elif "passw" in err.errors()[0]['loc']:
                return False, "La contraseña debe tener entre 8 y 255 caracteres"
    
    def registrar(self, nombre, email, passw):
        try:
            data = UsuarioRegistro_Schema(nombre=nombre, email=email, passw=passw)
            is_valid, mensaje = self.model.registrar(data.nombre, data.email, data.passw)
            return is_valid, mensaje
            
        except ValidationError as err:
            print(f"Error de validación: {err}")
            if "nombre" in err.errors()[0]['loc']:
                return False, "El nombre debe tener de 3 a 50 caracteres"
            
            elif "email" in err.errors()[0]['loc']:
                return False, "El correo electrónico no es válido"
            
            elif "passw" in err.errors()[0]['loc']:
                return False, "La contraseña debe tener entre 8 y 255 caracteres"
    
    def enviar_codigo(self, email, codigo):
        try:
            data = UsuarioBase_Schema(email=email)
            
            if self.model.data(email):
                return EmailSender.enviar_codigo(data.email, codigo)
            else:
                return False, "No existe una cuenta asociada a este correo electrónico"
        
        except Exception as err:
            print(f"Error de validación: {err}")
            return False, "El correo electrónico no es válido"

    def cambiar_passw(self, email, codigo_dado, codigo_solicitado, nueva_passw):
        try:
            data = UsuarioRecuperarPassw_Schema(codigo=codigo_dado, passw=nueva_passw)
            
            if data.codigo == codigo_solicitado:
                return self.model.actualizar_passw(email, data.passw)
            else:
                return False, "El código es incorrecto"

        except ValidationError as err:
            print(f"Error de validación: {err}")
            if "codigo" in err.errors()[0]['loc']:
                return False, "El código debe ser un número de 6 dígitos"
            
            elif "passw" in err.errors()[0]['loc']:
                return False, "La contraseña debe tener entre 8 y 255 caracteres"
    
    def eliminar_cuenta(self, email):
        return self.model.eliminar(email)