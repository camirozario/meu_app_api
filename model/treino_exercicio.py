from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base

class TreinoExercicio(Base):
    __tablename__ = "treino_exercicio"

    id = Column(Integer, primary_key=True)
    treino_id = Column(Integer, ForeignKey("treino.id"))
    exercicio_id = Column(Integer, ForeignKey("exercicio.id"))
    sets = Column(Integer)
    reps = Column(Integer)

    treino = relationship("Treino", back_populates="exercicios_associados")
    exercicio = relationship("Exercicio", back_populates="em_treinos")