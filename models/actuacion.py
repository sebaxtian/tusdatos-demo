from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class ActuacionCreateModel(BaseModel):
    id_detalle: int
    id_proceso: int
    num_proceso: str
    id_judicatura: str
    codigo_actuacion: int
    data_actuacion: Dict
    created: datetime
    updated: datetime


class ActuacionModel(BaseModel):
    id: int
    id_detalle: int
    id_proceso: int
    num_proceso: str
    id_judicatura: str
    codigo_actuacion: int
    data_actuacion: Dict
    created: datetime
    updated: datetime


class ActuacionPaginationModel(BaseModel):
    count: int
    skip: int
    limit: int
    actuaciones: list[ActuacionModel]
