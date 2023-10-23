from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# declara as tabelas
from models.base import Base
from models.pessoa import Pessoa

# conecta a base de dados
pg_db = os.environ['POSTGRES_DB']
pg_user = os.environ['POSTGRES_USER']
pg_pwd = os.environ['POSTGRES_PASSWORD']
database_path=f'postgresql://{pg_user}:{pg_pwd}@localhost:5432/{pg_db}'
engine = create_engine(database_path, echo=False)

# cria a SQLAlchemy session factory
Session = sessionmaker(bind=engine)

# cria as tabelas
# Base.metadata.create_all(engine)
