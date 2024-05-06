from datetime import timedelta
from typing import List

import pendulum
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from crud.estado_consulta import EstadoConsultaCRUD
from crud.proceso import ProcesoCRUD
from deps.cache import create_cache
from deps.database import get_db
from deps.jwtuser import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user
from deps.settings import get_settings
from models.entidad import EntidadModel, TipoEntidad
from models.estado_consulta import EstadoConsultaModel, EstadoConsultaCreateModel
from models.proceso import ProcesoPaginationModel
from models.token import TokenModel
from models.user import UserModel
from scraping_procesos import ScrapingProcesos
from settings import Settings

app = FastAPI(
    dependencies=[Depends(get_settings), Depends(get_db)],
    lifespan=create_cache,
)

# noinspection PyTypeChecker
app.add_middleware(GZipMiddleware, minimum_size=500)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)) -> TokenModel:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenModel(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=UserModel, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@app.get("/", status_code=status.HTTP_200_OK)
@cache(namespace="root", expire=pendulum.duration(minutes=5).seconds)
async def root(settings: Settings = Depends(get_settings)) -> JSONResponse:
    return JSONResponse({"app_name": settings.app_name, "env": settings.env, "date_time": pendulum.now().isoformat()})


@app.delete("/clear-cache", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_user)])
async def clear():
    await FastAPICache.clear(namespace="root")


@app.post("/consultar/procesos", response_model=EstadoConsultaModel, status_code=status.HTTP_202_ACCEPTED,
          dependencies=[Depends(get_current_active_user)])
async def consultar_procesos(entidad: EntidadModel, background_tasks: BackgroundTasks,
                             db: Session = Depends(get_db)) -> EstadoConsultaModel:
    # Realiza la consulta solo cuando no existe una consulta previa ejecutandose
    estado_consulta = EstadoConsultaCRUD.is_consulta_activa(db, entidad.hid, entidad.tipo.value)
    if estado_consulta:
        return estado_consulta

    # Cuando no existe consulta previa realiza la consulta
    estado_consulta = EstadoConsultaCRUD.create(db,
                                                EstadoConsultaCreateModel(hid_entidad=entidad.hid,
                                                                          tipo_entidad=entidad.tipo.value,
                                                                          created=pendulum.now(),
                                                                          updated=pendulum.now()))

    # Ejecuta el proceso de consulta en background
    background_tasks.add_task(ScrapingProcesos(estado_consulta.id).run_scraping, entidad)

    # Retorna el estados de consultas
    return estado_consulta


@app.post("/consultar/procesos/batch", response_model=List[EstadoConsultaModel], status_code=status.HTTP_202_ACCEPTED,
          dependencies=[Depends(get_current_active_user)])
async def consultar_procesos_batch(entidades: List[EntidadModel], background_tasks: BackgroundTasks,
                                   db: Session = Depends(get_db)) -> List[EstadoConsultaModel]:
    # Lista de estados de consultas
    estado_consultas: List[EstadoConsultaModel] = []

    # Validar el liminte maximo de entidades permitidas
    if len(entidades) < 16:
        # Por cada entidad
        for entidad in entidades:

            # Realiza la consulta solo cuando no existe una consulta previa ejecutandose
            estado_consulta = EstadoConsultaCRUD.is_consulta_activa(db, entidad.hid, entidad.tipo.value)
            if estado_consulta:
                # Lista de estados de consultas
                estado_consultas.append(estado_consulta)
                continue

            # Cuando no existe consulta previa realiza la consulta
            estado_consulta = EstadoConsultaCRUD.create(db,
                                                        EstadoConsultaCreateModel(hid_entidad=entidad.hid,
                                                                                  tipo_entidad=entidad.tipo.value,
                                                                                  created=pendulum.now(),
                                                                                  updated=pendulum.now()))

            # Ejecuta el proceso de consulta en background
            background_tasks.add_task(ScrapingProcesos(estado_consulta.id).run_scraping, entidad)

            # Lista de estados de consultas
            estado_consultas.append(estado_consulta)

    # Retorna la lista de estados de consultas
    return estado_consultas


@app.get("/{tipo_entidad}/{hid_entidad}/procesos", response_model=ProcesoPaginationModel, status_code=status.HTTP_200_OK,
         dependencies=[Depends(get_current_active_user)])
@cache(namespace="procesos", expire=pendulum.duration(minutes=5).seconds)
async def procesos(hid_entidad: str, tipo_entidad: str, skip: int = 0, limit: int = None,
                   db: Session = Depends(get_db)) -> ProcesoPaginationModel:
    procesos = ProcesoCRUD.read_procesos(db, hid_entidad=hid_entidad, tipo_entidad=tipo_entidad, skip=skip, limit=limit)
    return procesos
