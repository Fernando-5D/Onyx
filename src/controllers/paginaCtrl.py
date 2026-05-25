from models.PaginaModel import PaginaModel
from models.Database import Database

class PaginaCtrl:
    def __init__(self):
        self.model = PaginaModel(Database())
    
    def obtener_pajina(self, email):
        return self.model.data(email)

    def crear_pagina(self, email, titulo, contenido):
        if contenido.strip() == "":
            return False, "El contenido no puede estar vacio"
        return self.model.crear(email, titulo, contenido)

    def editar_pagina(self, id_pagina, nombre, contenido):
        if nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        if contenido.strip() == "":
            return False, "El contenido no puede estar vacío"

        return self.model.editar(id_pagina, nombre, contenido)

    def eliminar_pagina(self, id_pagina):
        return self.model.eliminar(id_pagina)
