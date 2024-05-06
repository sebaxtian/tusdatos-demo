from sqlalchemy import Column, Integer, String, DateTime, JSON

from db.connection import Base


class ActuacionSchema(Base):
    __tablename__ = "actuacion"

    id = Column(Integer, primary_key=True, index=True)
    id_detalle = Column(Integer, nullable=False)
    id_proceso = Column(Integer, nullable=False)
    num_proceso = Column(String, nullable=False)
    id_judicatura = Column(String, nullable=False)
    codigo_actuacion = Column(Integer, nullable=False)
    data_actuacion = Column(JSON, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
