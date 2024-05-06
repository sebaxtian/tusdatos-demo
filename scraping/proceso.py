from typing import Dict, List

from scraping.detalle import Detalle


class Proceso:

    def __init__(self, pid: int, id_juicio: str, data_proceso: Dict):
        self.__pid = pid
        self.__id_juicio = id_juicio
        self.__data_proceso = data_proceso
        self.__detalles: List[Detalle] = []

    @property
    def pid(self) -> int:
        return self.__pid

    @property
    def num_proceso(self) -> str:
        return self.__id_juicio

    @property
    def data_proceso(self) -> Dict:
        return self.__data_proceso

    @property
    def detalles(self) -> List:
        return self.__detalles

    @detalles.setter
    def detalles(self, detalles: List[Detalle]):
        self.__detalles = detalles

    def add_detalle(self, detalle: Detalle):
        self.__detalles.append(detalle)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__pid == other.__pid and self.__id_juicio == other.__id_juicio

    def __str__(self):
        return f"{self.__pid} - {self.__id_juicio}"

    def __repr__(self):
        return self.__str__()
