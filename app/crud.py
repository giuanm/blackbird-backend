from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from .models import AdminType, get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted==False).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email, models.User.is_deleted==False).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_deleted==False).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, current_user: models.User):
    if user.admin_type == AdminType.adm_sys:
        raise HTTPException(status_code=403, detail="Não é permitido criar usuários adm_sys via API.")
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        company_id=current_user.company_id,
        rol=user.rol,
        level=user.level
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).filter(models.Company.is_deleted == False).offset(skip).limit(limit).all()


def create_company(db: Session, company: schemas.CompanyCreate):  # Corrigido nome da função
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_user(db: Session, user_id: int, user_update: schemas.UserBase):  # Alterado para UserBase
    db_user = get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for key, value in user_update.dict(exclude={"password", "email", "is_deleted"}, exclude_unset=True).items():  # Exclui is_deleted
        setattr(db_user, key, value)
    if user_update.password:
        hashed_password = get_password_hash(user_update.password)
        setattr(db_user, "hashed_password", hashed_password)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.is_deleted = not user.is_deleted
    db.commit()
    return {"message": "Status do usuário alterado"}


def delete_company(db: Session, company_id: int):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    company.is_deleted = not company.is_deleted
    db.commit()
    return {"message": "Status da empresa alterado"}


def update_company(db: Session, company_id: int, company_update: schemas.CompanyBase):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()

    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in company_update.dict(exclude_unset=True).items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company
