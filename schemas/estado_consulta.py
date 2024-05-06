import pendulum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates

from db.connection import Base
from models.entidad import TipoEntidad
from models.estado_consulta import Status


class EstadoConsultaSchema(Base):
    __tablename__ = "estado_consulta"

    id = Column(Integer, primary_key=True, index=True)
    hid_entidad = Column(String, nullable=False)
    tipo_entidad = Column(String, nullable=False)
    status = Column(String, nullable=False, default=Status.ACCEPTED.value)
    duration = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)

    # Simple tipo_entidad validation
    @validates("tipo_entidad")
    def validate_tipo_entidad(self, key, tipo_entidad):
        if tipo_entidad not in TipoEntidad:
            raise ValueError("failed simple tipo_entidad validation")
        return tipo_entidad

    # Simple status validation
    @validates("status")
    def validate_status(self, key, status):
        if status not in Status:
            raise ValueError("failed simple status validation")
        return status

    # Simple duration validation
    @validates("duration")
    def validate_duration(self, key, duration):
        if duration >= 0:
            raise ValueError("failed simple duration validation")
        return duration
