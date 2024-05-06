from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from models.entidad import TipoEntidad


class Status(Enum):
    ACCEPTED = 'ACCEPTED'
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'


class EstadoConsultaCreateModel(BaseModel):
    hid_entidad: str
    tipo_entidad: str
    created: datetime
    updated: datetime


class EstadoConsultaModel(BaseModel):
    id: int
    hid_entidad: str
    tipo_entidad: TipoEntidad
    status: Status
    duration: int
    created: datetime
    updated: datetime
