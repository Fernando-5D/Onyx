from models.PaginaModel import PaginaModel
from models.Database import Database

class PaginaCtrl:
    def __init__(self):
        self.model = PaginaModel(Database())


    def crear_pagina(self, id_usuario, nombre, contenido):
        if nombre.strip() == "":
            return False, "El nombre no puede estar vacio"
        if contenido.strip() == "":
            return False, "El contenido no puede estar vacio"
        return self.model.crear(id_usuario, nombre, contenido)


    def editar_pagina(self, id_pagina, nombre, contenido):
        if nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        if contenido.strip() == "":
            return False, "El contenido no puede estar vacío"

        return self.model.editar(id_pagina, nombre, contenido)


    def eliminar_pagina(self, id_pagina):
        return self.model.eliminar(id_pagina)
