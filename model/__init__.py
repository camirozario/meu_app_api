from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importa a base de todos os modelos
from model.base import Base

# ⚠️ Corrigir este import para usar "Treino" em vez de "Workout"
from model.treino import Treino  # Supondo que o arquivo esteja em model/treino.py
from model.treino_exercicio import TreinoExercicio
from model.exercicio import Exercicio

# Caminho do banco de dados
db_path = "database/"
if not os.path.exists(db_path):
    os.makedirs(db_path)  # Cria o diretório se não existir

# URL de conexão com o banco SQLite
db_url = f'sqlite:///{db_path}db.sqlite3'

# Cria a engine de conexão
engine = create_engine(db_url, echo=False)

# Cria uma sessão para interagir com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ainda não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas conforme os modelos definidos
Base.metadata.create_all(engine)