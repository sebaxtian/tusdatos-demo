from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class ProcesoCreateModel(BaseModel):
    hid_entidad: str
    tipo_entidad: str
    pid: int
    num_proceso: str
    data_proceso: Dict
    created: datetime
    updated: datetime


class ProcesoModel(BaseModel):
    id: int
    hid_entidad: str
    tipo_entidad: str
    pid: int
    num_proceso: str
    data_proceso: Dict
    created: datetime
    updated: datetime


class ProcesoPaginationModel(BaseModel):
    count: int
    skip: int
    limit: int
    procesos: list[ProcesoModel]
