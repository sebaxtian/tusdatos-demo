from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class DetalleCreateModel(BaseModel):
    id_proceso: int
    num_proceso: str
    id_judicatura: str
    id_incidente_judicatura: int
    id_movimiento_juicio_incidente: int
    data_detalle: Dict
    created: datetime
    updated: datetime


class DetalleModel(BaseModel):
    id: int
    id_proceso: int
    num_proceso: str
    id_judicatura: str
    id_incidente_judicatura: int
    id_movimiento_juicio_incidente: int
    data_detalle: Dict
    created: datetime
    updated: datetime


class DetallePaginationModel(BaseModel):
    count: int
    skip: int
    limit: int
    detalles: list[DetalleModel]
