from typing import List

import pendulum
from sqlalchemy.orm import Session

from models.actuacion import ActuacionCreateModel, ActuacionModel, ActuacionPaginationModel
from schemas.actuacion import ActuacionSchema


class ActuacionCRUD:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ActuacionCRUD, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def create(db: Session, actuacion: ActuacionCreateModel) -> ActuacionModel:
        ActuacionSchema.metadata.create_all(bind=db.get_bind())

        # Busca la actuacion
        # noinspection PyTypeChecker
        db_actuacion: ActuacionSchema = db.query(ActuacionSchema).filter(
            ActuacionSchema.id_proceso == actuacion.id_proceso,
            ActuacionSchema.id_detalle == actuacion.id_detalle,
            ActuacionSchema.id_judicatura == actuacion.id_judicatura,
            ActuacionSchema.codigo_actuacion == actuacion.codigo_actuacion
        ).first()

        if not db_actuacion:
            # Crea el detalle si no existe
            db_actuacion = ActuacionSchema(**actuacion.dict())
            db.add(db_actuacion)
        else:
            # Actualiza la actuacion existente
            # noinspection PyTypeChecker
            db.query(ActuacionSchema).filter(ActuacionSchema.id == db_actuacion.id).update(
                {
                    ActuacionSchema.num_proceso: actuacion.num_proceso,
                    ActuacionSchema.id_judicatura: actuacion.id_judicatura,
                    ActuacionSchema.codigo_actuacion: actuacion.codigo_actuacion,
                    ActuacionSchema.data_actuacion: actuacion.data_actuacion,
                    ActuacionSchema.updated: pendulum.now()
                }
            )
            # noinspection PyTypeChecker
            db_actuacion: ActuacionSchema = db.query(ActuacionSchema).filter(
                ActuacionSchema.id_proceso == actuacion.id_proceso,
                ActuacionSchema.id_detalle == actuacion.id_detalle,
                ActuacionSchema.id_judicatura == actuacion.id_judicatura,
                ActuacionSchema.codigo_actuacion == actuacion.codigo_actuacion
            ).first()

        db.commit()
        db.refresh(db_actuacion)

        return ActuacionModel.validate(db_actuacion.__dict__)

    def read_actuaciones(db: Session, id_proceso: int, id_detalle: int, skip: int = 0, limit: int = None) -> ActuacionPaginationModel:

        # noinspection PyTypeChecker
        actuaciones: List[ActuacionSchema] = db.query(ActuacionSchema).filter(
            ActuacionSchema.id_proceso == id_proceso,
            ActuacionSchema.id_detalle == id_detalle
        ).offset(skip).limit(limit).all()

        count = len(actuaciones)
        limit = count if not limit or limit > count else limit

        actuaciones: List[ActuacionModel] = [ActuacionModel.validate(actuacion.__dict__) for actuacion in actuaciones]

        return ActuacionPaginationModel.validate({
            "count": count,
            "skip": skip,
            "limit": limit,
            "actuaciones": actuaciones
        })
