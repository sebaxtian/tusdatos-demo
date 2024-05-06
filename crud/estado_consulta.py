import pendulum
from sqlalchemy.orm import Session

from models.estado_consulta import EstadoConsultaModel, EstadoConsultaCreateModel, Status
from schemas.estado_consulta import EstadoConsultaSchema


class EstadoConsultaCRUD:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EstadoConsultaCRUD, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def is_consulta_activa(db: Session, hid_entidad: str, tipo_entidad: str) -> EstadoConsultaModel | None:
        EstadoConsultaSchema.metadata.create_all(bind=db.get_bind())
        # noinspection PyTypeChecker
        estado_consulta: EstadoConsultaSchema = db.query(EstadoConsultaSchema).filter(
            EstadoConsultaSchema.hid_entidad == hid_entidad, EstadoConsultaSchema.tipo_entidad == tipo_entidad,
            EstadoConsultaSchema.created > pendulum.now().subtract(minutes=5)).order_by(
            EstadoConsultaSchema.id.desc()).first()
        if estado_consulta:
            return EstadoConsultaModel.validate(estado_consulta.__dict__)

        return None

    @staticmethod
    def create(db: Session, estado_consulta: EstadoConsultaCreateModel) -> EstadoConsultaModel:
        EstadoConsultaSchema.metadata.create_all(bind=db.get_bind())
        estado_consulta = EstadoConsultaSchema(**estado_consulta.dict())
        db.add(estado_consulta)
        db.commit()
        db.refresh(estado_consulta)
        return EstadoConsultaModel.validate(estado_consulta.__dict__)

    @staticmethod
    def update_estado(db: Session, id_estado_consulta: int, status: Status) -> EstadoConsultaModel:
        EstadoConsultaSchema.metadata.create_all(bind=db.get_bind())
        # noinspection PyTypeChecker
        db.query(EstadoConsultaSchema).filter(EstadoConsultaSchema.id == id_estado_consulta).update(
            {EstadoConsultaSchema.status: status.value, EstadoConsultaSchema.updated: pendulum.now()})
        db.commit()
        # noinspection PyTypeChecker
        estado_consulta: EstadoConsultaSchema = db.query(EstadoConsultaSchema).filter(
            EstadoConsultaSchema.id == id_estado_consulta).first()
        if status == Status.FINISHED:
            duration = (estado_consulta.updated - estado_consulta.created).seconds
            # noinspection PyTypeChecker
            db.query(EstadoConsultaSchema).filter(EstadoConsultaSchema.id == id_estado_consulta).update(
                {EstadoConsultaSchema.duration: duration})
            db.commit()
            db.refresh(estado_consulta)
        return EstadoConsultaModel.validate(estado_consulta.__dict__)
