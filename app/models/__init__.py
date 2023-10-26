from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# declara as tabelas
from models.base import Base
from models.pessoa import Pessoa

# prepara a string de conxeão a base de dados
pg_host = os.environ['POSTGRES_HOST']
pg_port = os.environ['POSTGRES_PORT']
pg_db = os.environ['POSTGRES_DB']
pg_user = os.environ['POSTGRES_USER']
pg_pwd = os.environ['POSTGRES_PASSWORD']
database_path=f'postgresql://{pg_user}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}'

# conecta a base de dados
engine = create_engine(database_path, echo=False)

# cria a SQLAlchemy session factory
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# cria as tabelas
# realizamos a criação da tabela diretamente no banco via sql
# pois o create_all() causa race conditions quando usados multiplos workers.
# Base.metadata.create_all(engine)
