from enum import Enum

from pydantic import BaseModel


class TipoEntidad(Enum):
    ACTOR_OFENDIDO = 'ACTOR_OFENDIDO'
    DEMANDADO_PROCESADO = 'DEMANDADO_PROCESADO'


class EntidadModel(BaseModel):
    hid: str
    tipo: TipoEntidad
