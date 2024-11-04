from argon2 import PasswordHasher  # Importe o Argon2
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import enum

from .database import Base


ph = PasswordHasher()  # Criar uma instância do PasswordHasher


class AdminType(enum.Enum):
    adm_sys = 1
    adm_comp = 2


class RoleEnum(enum.Enum):
    adm = "adm"
    vet = "vet"
    med = "med"
    cont = "cont"
    adv = "adv"


class LevelEnum(enum.Enum):
    l1 = "l1"
    l2 = "l2"
    l3 = "l3"
    l4 = "l4"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    is_deleted = Column(Boolean, default=False, server_default="0", nullable=False)

    users = relationship("User", back_populates="company")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    phone = Column(String(20))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    company_id = Column(Integer, ForeignKey("companies.id"))
    rol = Column(Enum(RoleEnum, name="rol_enum"))
    level = Column(Enum(LevelEnum, name="level_enum"))
    is_deleted = Column(Boolean, default=False, server_default="0", nullable=False)
    admin_type = Column(Enum(AdminType), nullable=True)

    company = relationship("Company", back_populates="users")

    def verify_password(self, plain_password):
        try:
            ph.verify(self.hashed_password, plain_password)
            return True
        except Exception as e:
            print(f"Erro na verificação: {e}")
            return False


def get_password_hash(password):
    return ph.hash(password)
