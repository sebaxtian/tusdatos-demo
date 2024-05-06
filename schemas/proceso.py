from sqlalchemy import Column, Integer, String, DateTime, JSON

from db.connection import Base


class ProcesoSchema(Base):
    __tablename__ = "proceso"

    id = Column(Integer, primary_key=True, index=True)
    hid_entidad = Column(String, nullable=False)
    tipo_entidad = Column(String, nullable=False)
    pid = Column(Integer, nullable=False)
    num_proceso = Column(String, nullable=False)
    data_proceso = Column(JSON, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
