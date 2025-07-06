from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from model.base import Base

class Exercicio(Base):
    __tablename__ = "exercicio"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), unique=True)
    musculo = Column(String(50))
    descricao = Column(String(255))
    thumbnail = Column(String(255))

    # Relacionamento com TreinoExercicio
    em_treinos = relationship("TreinoExercicio", back_populates="exercicio")