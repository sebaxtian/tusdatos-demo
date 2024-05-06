from typing import List

import pendulum
from sqlalchemy.orm import Session

from models.detalle import DetalleCreateModel, DetalleModel, DetallePaginationModel
from schemas.detalle import DetalleSchema


class DetalleCRUD:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DetalleCRUD, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def create(db: Session, detalle: DetalleCreateModel) -> DetalleModel:
        DetalleSchema.metadata.create_all(bind=db.get_bind())

        # Busca el detalle
        # noinspection PyTypeChecker
        db_detalle: DetalleSchema = db.query(DetalleSchema).filter(
            DetalleSchema.id_proceso == detalle.id_proceso,
            DetalleSchema.id_judicatura == detalle.id_judicatura,
            DetalleSchema.id_incidente_judicatura == detalle.id_incidente_judicatura,
            DetalleSchema.id_movimiento_juicio_incidente == detalle.id_movimiento_juicio_incidente,
        ).first()

        if not db_detalle:
            # Crea el detalle si no existe
            db_detalle = DetalleSchema(**detalle.dict())
            db.add(db_detalle)
        else:
            # Actualiza el detalle existente
            # noinspection PyTypeChecker
            db.query(DetalleSchema).filter(DetalleSchema.id == db_detalle.id).update(
                {
                    DetalleSchema.num_proceso: detalle.num_proceso,
                    DetalleSchema.id_judicatura: detalle.id_judicatura,
                    DetalleSchema.id_incidente_judicatura: detalle.id_incidente_judicatura,
                    DetalleSchema.id_movimiento_juicio_incidente: detalle.id_movimiento_juicio_incidente,
                    DetalleSchema.data_detalle: detalle.data_detalle,
                    DetalleSchema.updated: pendulum.now()
                }
            )
            # noinspection PyTypeChecker
            db_detalle: DetalleSchema = db.query(DetalleSchema).filter(
                DetalleSchema.id_proceso == detalle.id_proceso,
                DetalleSchema.id_judicatura == detalle.id_judicatura,
                DetalleSchema.id_incidente_judicatura == detalle.id_incidente_judicatura,
                DetalleSchema.id_movimiento_juicio_incidente == detalle.id_movimiento_juicio_incidente,
            ).first()

        db.commit()
        db.refresh(db_detalle)

        return DetalleModel.validate(db_detalle.__dict__)

    def read_detalles(db: Session, id_proceso: int, skip: int = 0, limit: int = None) -> DetallePaginationModel:

        # noinspection PyTypeChecker
        detalles: List[DetalleSchema] = db.query(DetalleSchema).filter(
            DetalleSchema.id_proceso == id_proceso
        ).offset(skip).limit(limit).all()

        count = len(detalles)
        limit = count if not limit or limit > count else limit

        detalles: List[DetalleModel] = [DetalleModel.validate(detalle.__dict__) for detalle in detalles]

        return DetallePaginationModel.validate({
            "count": count,
            "skip": skip,
            "limit": limit,
            "detalles": detalles
        })
