from scraping.entidad import Entidad


class DemandadoProcesado(Entidad):

    def __init__(self, nombre: str, hid: str):
        super().__init__(nombre, hid)

    def __str__(self):
        return f"Nombre: {self.nombre}, Identificacion: {self.hid}"

    def __repr__(self):
        return f"Nombre: {self.nombre}, Identificacion: {self.hid}"
