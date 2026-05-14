from pydantic import ValidationError
from models.UsuarioModel import UsuarioModel
from models.Database import Database
from models.schemas import UsuarioBase_Schema, UsuarioRegistro_Schema

class UsuarioCtrl:
    def __init__(self):
        self.model = UsuarioModel(Database())
    
    def iniciar_sesion(self, email, passw):
        try:
            data = UsuarioBase_Schema(email=email, passw=passw)
            is_valid, mensaje = self.model.iniciar_sesion(data.email, data.passw)
            return is_valid, mensaje
            
        except ValidationError as err:
            print(f"Error de validación: {err}")
            if "email" in err.errors()[0]['loc']:
                return False, "El correo electrónico no es válido o excede los 255 caracteres"
            
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
                return False, "El correo electrónico no es válido o excede los 255 caracteres"
            
            elif "passw" in err.errors()[0]['loc']:
                return False, "La contraseña debe tener entre 8 y 255 caracteres"