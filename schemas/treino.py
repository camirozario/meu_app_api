# schemas/treino.py
from pydantic import BaseModel
from typing import List
from model.treino import Treino

class TreinoExercicioSchema(BaseModel):
    exercicio_id: int
    sets: int
    reps: int

class TreinoSchema(BaseModel):
    titulo: str
    exercicios: List[TreinoExercicioSchema]

class TreinoViewSchema(BaseModel):
    id: int
    titulo: str
    total_exercicios: int
    exercicios: List[TreinoExercicioSchema]

class ListagemTreinosSchema(BaseModel):
    treinos: List[TreinoViewSchema]



def apresenta_treino(treino: Treino):
    return {
        "id": treino.id,
        "titulo": treino.titulo,
        "total_exercicios": len(treino.exercicios_associados),
        "exercicios": [
            {
                "exercicio_id": te.exercicio_id,
                "sets": te.sets,
                "reps": te.reps
            }
            for te in treino.exercicios_associados
        ]
    }

def apresenta_treinos(treinos: List[Treino]):
    return {
        "treinos": [apresenta_treino(treino) for treino in treinos]
    }

