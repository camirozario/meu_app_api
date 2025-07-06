from pydantic import BaseModel
from typing import Optional, List
from model.exercicio import Exercicio

class ExercicioSchema(BaseModel):
    titulo: str
    musculo: str
    descricao: Optional[str] = ""
    thumbnail: Optional[str] = ""

class ExercicioBuscaSchema(BaseModel):
    titulo: str

class ListagemExerciciosSchema(BaseModel):
    exercicios: List[ExercicioSchema]

def apresenta_exercicios(exercicios: List[Exercicio]):
    return {
        "exercicios": [
            {
                "id": e.id,
                "titulo": e.titulo,
                "musculo": e.musculo,
                "descricao": e.descricao,
                "thumbnail": e.thumbnail,
            } for e in exercicios
        ]
    }

class ExercicioViewSchema(BaseModel):
    id: int
    titulo: str
    musculo: str
    descricao: Optional[str]
    thumbnail: Optional[str]
    #treino: Optional[TreinoSchema]

class ExercicioDelSchema(BaseModel):
    message: str
    titulo: str

def apresenta_exercicio(exercicio: Exercicio):
    return {
        "id": exercicio.id,
        "titulo": exercicio.titulo,
        "musculo": exercicio.musculo,
        "descricao": exercicio.descricao,
        "thumbnail": exercicio.thumbnail,
        "treino_id": exercicio.treino_id
    }