from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from model.base import Base

class Treino(Base):
    __tablename__ = "treino"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)

    # Relacionamento com TreinoExercicio
    exercicios_associados = relationship("TreinoExercicio", back_populates="treino", cascade="all, delete-orphan")
