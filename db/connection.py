from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from deps.settings import get_settings
from settings import Settings

settings: Settings = get_settings()

db_sqlite = {"dev": "/db/data/tusdatos-api-mvp.db", "prod": ""}

# SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite://{db_sqlite[settings.env]}"

# PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Database Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()
class Base(DeclarativeBase):
    pass


Base.metadata.create_all(bind=engine)

# Demo User: admin, admin
# with SessionLocal() as session:
#     from schemas.user import UserSchema
#     Base.metadata.create_all(bind=engine)
#     UserSchema.metadata.create_all(bind=db.get_bind())
#     user = UserSchema(
#         username="admin",
#         email="admin@example.com",
#         full_name="Admin Tusdatos",
#         hashed_password="$2y$10$v1FX3CpwMliT1A7KxSv2vu1KqZsagOe42Z6DC0MFS5D7VhxF85PHu"
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)
