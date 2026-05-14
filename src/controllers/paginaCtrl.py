from models.UsuarioModel import UsuarioModel
from models.Database import Database

class PaginaCtrl:
    def __init__(self):
        self.model = UsuarioModel(Database())
    
    def obtener_data(self, email, campo = "*"):
        return self.model.data(email, campo)