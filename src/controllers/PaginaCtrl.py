from pydantic import ValidationError
from models.PaginaModel import PaginaModel
from models.Database import Database

class PaginaCtrl:
    def __init__(self):
        self.model = PaginaModel(Database())
    
    def obtener_data(self, email_usuario, id = None):
        return self.model.data(email_usuario, id)

    def crear_pagina(self, email_usuario, titulo, contenido):
        return self.model.crear(email_usuario, titulo if titulo != "" else "Sin Titulo", contenido)

    def editar_pagina(self, id, titulo = "Sin Titulo", contenido = ""):
        return self.model.editar(id, titulo, contenido)

    def eliminar_pagina(self, id):
        return self.model.eliminar(id)
