from typing import Dict, List

from scraping.actuacion import Actuacion


class Detalle:

    def __init__(self, pid: int, num_proceso: str, id_judicatura: str, id_incidente_judicatura: int,
                 id_movimiento_juicio_incidente: int, data_detalle: Dict):
        self.__pid: int = pid
        self.__num_proceso: str = num_proceso
        self.__id_judicatura: str = id_judicatura
        self.__id_incidente_judicatura: int = id_incidente_judicatura
        self.__id_movimiento_juicio_incidente: int = id_movimiento_juicio_incidente
        self.__data_detalle: Dict = data_detalle
        self.__actuaciones: List[Actuacion] = []

    @property
    def pid(self) -> int:
        return self.__pid

    @property
    def num_proceso(self) -> str:
        return self.__num_proceso

    @property
    def id_judicatura(self) -> str:
        return self.__id_judicatura

    @property
    def id_incidente_judicatura(self) -> int:
        return self.__id_incidente_judicatura

    @property
    def id_movimiento_juicio_incidente(self) -> int:
        return self.__id_movimiento_juicio_incidente

    @property
    def data_detalle(self) -> Dict:
        return self.__data_detalle

    @property
    def actuaciones(self) -> List:
        return self.__actuaciones

    @actuaciones.setter
    def actuaciones(self, actuaciones: List[Actuacion]):
        self.__actuaciones = actuaciones

    def add_actuacion(self, actuacion: Actuacion):
        self.__actuaciones.append(actuacion)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__pid == other.__pid and self.__num_proceso == other.__num_proceso and self.__id_judicatura == other.__id_judicatura and self.__id_incidente_judicatura == other.__id_incidente_judicatura and self.__id_movimiento_juicio_incidente == other.__id_movimiento_juicio_incidente

    def __str__(self):
        return f"{self.__pid} - {self.__num_proceso} - {self.__id_judicatura}"

    def __repr__(self):
        return self.__str__()
