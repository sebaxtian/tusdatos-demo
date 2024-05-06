from typing import List

import pendulum
from sqlalchemy.orm import Session

from models.proceso import ProcesoCreateModel, ProcesoModel, ProcesoPaginationModel
from schemas.proceso import ProcesoSchema


class ProcesoCRUD:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProcesoCRUD, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def create(db: Session, proceso: ProcesoCreateModel) -> ProcesoModel:
        ProcesoSchema.metadata.create_all(bind=db.get_bind())

        # Busca el proceso
        # noinspection PyTypeChecker
        db_proceso: ProcesoSchema = db.query(ProcesoSchema).filter(
            ProcesoSchema.num_proceso == proceso.num_proceso).first()

        if not db_proceso:
            # Crea el proceso si no existe
            db_proceso = ProcesoSchema(**proceso.dict())
            db.add(db_proceso)
        else:
            # Actualiza el proceso existente
            # noinspection PyTypeChecker
            db.query(ProcesoSchema).filter(ProcesoSchema.num_proceso == db_proceso.num_proceso).update(
                {
                    ProcesoSchema.hid_entidad: proceso.hid_entidad,
                    ProcesoSchema.tipo_entidad: proceso.tipo_entidad,
                    ProcesoSchema.pid: proceso.pid,
                    ProcesoSchema.num_proceso: proceso.num_proceso,
                    ProcesoSchema.data_proceso: proceso.data_proceso,
                    ProcesoSchema.updated: pendulum.now()
                }
            )
            # noinspection PyTypeChecker
            db_proceso: ProcesoSchema = db.query(ProcesoSchema).filter(
                ProcesoSchema.num_proceso == proceso.num_proceso).first()

        db.commit()
        db.refresh(db_proceso)

        return ProcesoModel.validate(db_proceso.__dict__)

    def read_procesos(db: Session, hid_entidad: str, tipo_entidad: str, skip: int = 0,
                      limit: int = None) -> ProcesoPaginationModel:

        # noinspection PyTypeChecker
        procesos: List[ProcesoSchema] = db.query(ProcesoSchema).filter(
            ProcesoSchema.hid_entidad == hid_entidad, ProcesoSchema.tipo_entidad == tipo_entidad
        ).offset(skip).limit(limit).all()

        count = len(procesos)
        limit = count if not limit or limit > count else limit

        procesos: List[ProcesoModel] = [ProcesoModel.validate(proceso.__dict__) for proceso in procesos]

        return ProcesoPaginationModel.validate({
            "count": count,
            "skip": skip,
            "limit": limit,
            "procesos": procesos
        })
