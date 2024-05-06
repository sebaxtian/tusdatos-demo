import pendulum
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates
from db.connection import Base


class UserSchema(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String, nullable=False)
    created = Column(String, nullable=False, default=pendulum.now().isoformat())
    updated = Column(String, nullable=False, default=pendulum.now().isoformat(), onupdate=pendulum.now().isoformat())

    # Simple email validation
    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("failed simple email validation")
        return email
