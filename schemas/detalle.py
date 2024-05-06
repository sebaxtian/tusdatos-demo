from sqlalchemy import Column, Integer, String, DateTime, JSON

from db.connection import Base


class DetalleSchema(Base):
    __tablename__ = "detalle"

    id = Column(Integer, primary_key=True, index=True)
    id_proceso = Column(Integer, nullable=False)
    num_proceso = Column(String, nullable=False)
    id_judicatura = Column(String, nullable=False)
    id_incidente_judicatura = Column(Integer, nullable=False)
    id_movimiento_juicio_incidente = Column(Integer, nullable=False)
    data_detalle = Column(JSON, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
