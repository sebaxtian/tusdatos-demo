from typing import Dict


class Actuacion:

    def __init__(self, pid: int, num_proceso: str, id_judicatura: str, codigo_actuacion: str, data_actuacion: Dict):
        self.__pid = pid
        self.__num_proceso = num_proceso
        self.__id_judicatura = id_judicatura
        self.__codigo_actuacion = codigo_actuacion
        self.__data_actuacion = data_actuacion

    @property
    def pid(self):
        return self.__pid

    @property
    def num_proceso(self):
        return self.__num_proceso

    @property
    def id_judicatura(self):
        return self.__id_judicatura

    @property
    def codigo_actuacion(self):
        return self.__codigo_actuacion

    @property
    def data_actuacion(self):
        return self.__data_actuacion

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__pid == other.__pid and self.__num_proceso == other.__num_proceso and self.__id_judicatura == other.__id_judicatura and self.__codigo_actuacion == other.__codigo_actuacion

    def __str__(self):
        return f"{self.__pid} - {self.__num_proceso} - {self.__id_judicatura} - {self.__codigo_actuacion}"

    def __repr__(self):
        return self.__str__()
