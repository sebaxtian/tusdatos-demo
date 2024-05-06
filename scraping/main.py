from concurrent.futures import ThreadPoolExecutor, wait

import pendulum
from icecream import ic
from loguru import logger

from scraping.actor_ofendido import ActorOfendido
from scraping.consulta import Consulta
from scraping.demandado_procesado import DemandadoProcesado


def set_logger_datetime(record):
    record['time'] = pendulum.now("America/Bogota")


logger.configure(patcher=set_logger_datetime)
logger.add(
    f"logs/tusdatos_{pendulum.now('America/Bogota').to_date_string()}.log",
    rotation="1 MB",
    level="DEBUG",
    format="{time} - {level} - {name} - {message}",
)

ic.configureOutput(includeContext=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Proceso de Consulta
    consulta = Consulta()

    entidades = []

    # Entidades a consultar
    entidades.append(ActorOfendido("", "0968599020001"))
    entidades.append(DemandadoProcesado("", "1791251237001"))

    ic(entidades[0])
    ic(entidades[1])

    # Ejecutar la busqueda
    # procesos1 = consulta.buscar_procesos(entidades[0])
    # procesos2 = consulta.buscar_procesos(entidades[1])
    #
    # logger.debug(procesos1)
    # logger.debug(procesos2)

    # Crear un ThreadPoolExecutor
    num_threads = 15
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Enviar las tareas de requests para ejecutar en hilos
        threads = {}
        for i in range(len(entidades)):
            t = executor.submit(consulta.buscar_procesos, entidades[i])
            threads[f"Thread{i}"] = t

        # Esperar hasta completar todos los Threads
        wait(threads.values())

        # Print threads
        [ic(key, thread.result()) for key, thread in threads.items()]

        # Logger procesos
        logger.debug([proceso for thread in threads.values() for proceso in thread.result()])
