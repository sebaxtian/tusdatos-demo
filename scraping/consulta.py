from typing import Dict, List

import pendulum
from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy.orm import Session

import requests
from crud.estado_consulta import EstadoConsultaCRUD
from crud.proceso import ProcesoCRUD
from deps.database import get_db
from models.estado_consulta import EstadoConsultaModel, Status
from models.proceso import ProcesoCreateModel
from scraping.actuacion import Actuacion
from scraping.detalle import Detalle
from scraping.entidad import Entidad
from scraping.proceso import Proceso


def set_logger_datetime(record):
    record["time"] = pendulum.now("America/Bogota")


logger.configure(patcher=set_logger_datetime)
logger.add(
    f"logs/tusdatos_{pendulum.now('America/Bogota').to_date_string()}.log",
    rotation="1 MB",
    level="DEBUG",
    format="{time} - {level} - {name} - {message}",
)


class Consulta:

    URL_TOTAL_PROCESOS = ""
    URL_PROCESOS = ""
    URL_DETALLES = ""
    URL_ACTUACIONES = ""

    def __init__(self, id_estado_consulta: int = -1):
        self.id_estado_consulta = id_estado_consulta

    def update_estado_consulta(
        self, status: Status, db: Session = next(get_db())
    ) -> EstadoConsultaModel:
        return (
            EstadoConsultaCRUD.update_estado(db, self.id_estado_consulta, status)
            if self.id_estado_consulta != -1
            else None
        )

    def save_procesos(
        self, procesos: List[Proceso], db: Session = next(get_db())
    ) -> None:
        for proceso in procesos:
            proceso_model = ProcesoCreateModel(
                pid=proceso.pid,
                num_proceso=proceso.num_proceso,
                data_proceso=proceso.data_proceso,
                detalles=jsonable_encoder(proceso.detalles),
                created=pendulum.now(),
                updated=pendulum.now(),
            )
            ProcesoCRUD.create(db, proceso_model)

    def buscar_procesos(self, entidad: Entidad) -> List[Proceso]:
        # Update estado consulta
        self.update_estado_consulta(Status.STARTED)

        # Run the process
        procesos: List[Proceso] = self._nav_procesos(entidad)

        # Save procesos
        self.save_procesos(procesos)

    def _request_procesos(self, url_procesos: str, payload: Dict) -> List[Proceso]:
        # Procesos
        procesos: List[Proceso] = []

        consulta_procesos = requests.post(url_procesos, json=payload)
        # Extraer informacion de procesos
        if consulta_procesos.status_code == requests.codes.ok:
            for data in consulta_procesos.json():
                # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion
                procesos.append(proceso)
        else:
            # Log error
            logger.error(f"{consulta_procesos.status_code}: {consulta_procesos.text}")
            # Update estado consulta
            self.update_estado_consulta(Status.FAILED)

        return procesos

    def _nav_procesos(self, entidad: Entidad) -> List[Proceso]:
        # Update estado consulta
        self.update_estado_consulta(Status.RUNNING)

        # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion

        # Update estado consulta
        self.update_estado_consulta(Status.FINISHED)

        # Lista de Procesos
        return procesos

    def _nav_block_procesos(self, procesos: List[Proceso]) -> List[Proceso]:
        for proceso in procesos:
            proceso.detalles = self._nav_detalles(proceso)
        return procesos

    def _nav_detalles(self, proceso: Proceso) -> List[Detalle]:
        # URL Detalles
        url_detalles = f"{self.URL_DETALLES}/{proceso.num_proceso}"

        # Detalles
        detalles: List[Detalle] = []

        consulta_detalles = requests.get(url_detalles)
        if consulta_detalles.status_code == requests.codes.ok:
            for data in consulta_detalles.json():
                # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion
                detalles.append(detalle)
        else:
            # Log error
            logger.error(f"{consulta_detalles.status_code}: {consulta_detalles.text}")
            # Update estado consulta
            self.update_estado_consulta(Status.FAILED)

        # Lista de Detalles
        return detalles

    def _nav_actuaciones(self, detalle: Detalle) -> List[Actuacion]:
        # URL Actuaciones
        url_actuaciones = self.URL_ACTUACIONES
        # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion

        # Actuaciones
        actuaciones: List[Actuacion] = []

        # Consultar Actuaciones
        consulta_actuaciones = requests.post(url_actuaciones, json=payload)
        if consulta_actuaciones.status_code == requests.codes.ok:
            for data in consulta_actuaciones.json():
                # TODO: El codigo de este metodo solo se comparte al momento de sustentar la solucion en la presentacion
                actuaciones.append(actuacion)
        else:
            # Log error
            logger.error(
                f"{consulta_actuaciones.status_code}: {consulta_actuaciones.text}"
            )
            # Update estado consulta
            self.update_estado_consulta(Status.FAILED)

        # Lista de Actuaciones
        return actuaciones
