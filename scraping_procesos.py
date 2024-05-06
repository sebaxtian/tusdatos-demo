from typing import Dict

import pendulum
from loguru import logger
from sqlalchemy.orm import Session

import requests
from crud.actuacion import ActuacionCRUD
from crud.detalle import DetalleCRUD
from crud.estado_consulta import EstadoConsultaCRUD
from crud.proceso import ProcesoCRUD
from deps.database import get_db
from models.actuacion import ActuacionCreateModel
from models.detalle import DetalleCreateModel, DetalleModel
from models.entidad import EntidadModel
from models.estado_consulta import EstadoConsultaModel, Status
from models.proceso import ProcesoCreateModel, ProcesoModel


def set_logger_datetime(record):
    record["time"] = pendulum.now("America/Bogota")


logger.configure(patcher=set_logger_datetime)
logger.add(
    f"logs/tusdatos_{pendulum.now('America/Bogota').to_date_string()}.log",
    rotation="1 MB",
    level="DEBUG",
    format="{time} - {level} - {name} - {message}",
)


class ScrapingProcesos:
    URL_TOTAL_PROCESOS = ""
    URL_PROCESOS = ""
    URL_DETALLES = ""
    URL_ACTUACIONES = ""

    def __init__(self, id_estado_consulta: int = -1, db: Session = next(get_db())):
        self.id_estado_consulta: int = id_estado_consulta
        self.db_conn: Session = db
        # # Procesos
        # self.procesos: List[ProcesoModel] = []
        # # Detalles
        # self.detalles: List[DetalleModel] = []
        # # Actuaciones
        # self.actuaciones: List[DetalleModel] = []

    def update_estado_consulta(self, status: Status) -> EstadoConsultaModel:
        # Actualiza estado de la consulta
        return (
            EstadoConsultaCRUD.update_estado(
                self.db_conn, self.id_estado_consulta, status
            )
            if self.id_estado_consulta != -1
            else None
        )

    def run_scraping(self, entidad: EntidadModel) -> bool:
        # Update estado consulta
        self.update_estado_consulta(Status.STARTED)

        # Navegar procesos
        exito = self._nav_procesos(entidad)

        # Update estado consulta
        self.update_estado_consulta(Status.FINISHED)

        return exito

    def _request_procesos(
        self, url_procesos: str, payload: Dict, entidad: EntidadModel
    ) -> bool:
        exito = False
        # Consulta procesos
        consulta_procesos = requests.post(url_procesos, json=payload)
        # Extraer informacion de procesos
        if consulta_procesos.status_code == requests.codes.ok:
            # Por cada proceso
            for data in consulta_procesos.json():
                # Proceso para guardar
                proceso_model = ProcesoCreateModel(
                    hid_entidad=entidad.hid,
                    tipo_entidad=entidad.tipo.value,
                    # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion
                    data_proceso=data,
                    created=pendulum.now(),
                    updated=pendulum.now(),
                )
                # Guarda el proceso
                proceso: ProcesoModel = ProcesoCRUD.create(self.db_conn, proceso_model)

                # Navegar detalles
                exito = self._nav_detalles(proceso)
        else:
            # Log error
            logger.error(f"{consulta_procesos.status_code}: {consulta_procesos.text}")
            # Update estado consulta
            self.update_estado_consulta(Status.FAILED)

        return exito

    def _nav_procesos(self, entidad: EntidadModel) -> bool:
        exito = False
        # Update estado consulta
        self.update_estado_consulta(Status.RUNNING)

        # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion

        return exito

    def _nav_detalles(self, proceso: ProcesoModel) -> bool:
        exito = False
        # URL Detalles
        url_detalles = f"{self.URL_DETALLES}/{proceso.num_proceso}"
        # Consulta detalles
        consulta_detalles = requests.get(url_detalles)
        # Extraer informacion de detalle
        if consulta_detalles.status_code == requests.codes.ok:
            # Por cada detalle
            for data in consulta_detalles.json():
                # Detalle para guardar
                detalle_model = DetalleCreateModel(
                    id_proceso=proceso.id,
                    num_proceso=proceso.num_proceso,
                    # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion
                    data_detalle=data,
                    created=pendulum.now(),
                    updated=pendulum.now(),
                )
                # Guarda el detalle
                detalle: DetalleModel = DetalleCRUD.create(self.db_conn, detalle_model)

                # Navegar actuaciones
                exito = self._nav_actuaciones(detalle)
        else:
            # Log error
            logger.error(f"{consulta_detalles.status_code}: {consulta_detalles.text}")
            # Update estado consulta
            self.update_estado_consulta(Status.FAILED)

        return exito

    def _nav_actuaciones(self, detalle: DetalleModel) -> bool:
        exito = False
        # URL Actuaciones
        url_actuaciones = self.URL_ACTUACIONES
        # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion

        # Consultar Actuaciones
        consulta_actuaciones = requests.post(url_actuaciones, json=payload)
        # Extraer informacion de actuacion
        if consulta_actuaciones.status_code == requests.codes.ok:
            # Por cada actuacion
            for data in consulta_actuaciones.json():
                # Actuacion para guardar
                actuacion_model = ActuacionCreateModel(
                    id_detalle=detalle.id,
                    id_proceso=detalle.id_proceso,
                    num_proceso=detalle.num_proceso,
                    id_judicatura=detalle.id_judicatura,
                    # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion
                    data_actuacion=data,
                    created=pendulum.now(),
                    updated=pendulum.now(),
                )
                # Guarda la actuacion
                ActuacionCRUD.create(self.db_conn, actuacion_model)

                exito = True
        else:
            # Log error
            logger.error(
                f"{consulta_actuaciones.status_code}: {consulta_actuaciones.text}"
            )
            # Update estado consulta
            self.update_estado_consulta(Status.FAILED)

        return exito
