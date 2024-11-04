from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "admin"
DB_NAME = "blackbird"
DB_PORT = 3306

# URL de conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Cria o engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declara a base para os modelos
Base = declarative_base()


# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna a sessão do banco de dados
    finally:
        db.close() # Fecha a sessão ao finalizar