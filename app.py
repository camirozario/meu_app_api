from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
import os

from model import Session
from model.treino_exercicio import TreinoExercicio
from model.treino import Treino
from model.exercicio import Exercicio
from logger import logger

from schemas.exercicio import (
    ExercicioSchema,
    ExercicioViewSchema,
    ExercicioDelSchema,
    ListagemExerciciosSchema,
    apresenta_exercicio,
    apresenta_exercicios
)
from schemas.treino import (
    TreinoSchema,
    TreinoViewSchema,
    ListagemTreinosSchema,
    apresenta_treino,
    apresenta_treinos
)
from schemas.error import ErrorSchema

# Pasta para uploads
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Informações com markdown para documentação Swagger
info = Info(
    title="🏋️ Workout Builder API",
    version="1.0.0",
    description="""
## 📘️ API para Gerenciamento de Treinos

Esta API permite:
- ✅ Adicionar e listar **exercícios**
- 🏋️ Montar **treinos personalizados**
- 🖼️ Upload de imagens para exercícios
- 🔧 Testar todos os endpoints diretamente via Swagger UI

### 🔄 Como usar:
1. Use o botão **\"Try it out\"** ao lado de cada rota
2. Envie requisições e veja respostas em tempo real
3. Navegue pelas seções abaixo

> 🚧 _Esta API está em desenvolvimento. Funcionalidades adicionais serão adicionadas em breve._
"""
)

app = OpenAPI(__name__, info=info)
CORS(app)

# Tags com markdown
home_tag = Tag(
    name="Documentação",
    description="""
📚 Redireciona para a interface interativa da documentação:
- `/openapi/swagger` para Swagger UI
- `/openapi/redoc` para ReDoc
- `/openapi/rapidoc` para RapiDoc
"""
)

treino_tag = Tag(
    name="Treino",
    description="""
🎯 Operações relacionadas à montagem de treinos:
- Criar treinos com vários exercícios
- Visualizar treinos existentes
"""
)

exercicio_tag = Tag(
    name="Exercicio",
    description="""
💪 Gestão de exercícios:
- Adicionar, editar e remover exercícios
- Upload de imagem de miniatura (thumbnail)
- Buscar todos os exercícios cadastrados
"""
)

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para a documentação interativa"""
    return redirect('/openapi')

# ----------------- EXERCICIOS ------------------

@app.post('/upload_exercicio', tags=[exercicio_tag],
          responses={"200": ExercicioViewSchema, "400": ErrorSchema})
def upload_exercicio():
    """Adiciona um novo exercício a lista de exercícios"""
    try:
        titulo = request.form['titulo']
        musculo = request.form['musculo']
        descricao = request.form['descricao']
        imagem = request.files['imagem']

        filename = secure_filename(imagem.filename)
        imagem_path = os.path.join(UPLOAD_FOLDER, filename)
        imagem.save(imagem_path)

        thumbnail = f"{UPLOAD_FOLDER}/{filename}"

        exercicio = Exercicio(
            titulo=titulo,
            musculo=musculo,
            descricao=descricao,
            thumbnail=thumbnail
        )

        session = Session()
        session.add(exercicio)
        session.commit()
        return apresenta_exercicio(exercicio), 200

    except Exception as e:
        logger.error(f"Erro ao salvar exercício com imagem: {e}")
        return {"mesage": f"Erro ao salvar exercício: {str(e)}"}, 400

@app.delete('/exercicio', tags=[exercicio_tag],
            responses={"200": ExercicioDelSchema, "404": ErrorSchema})
def delete_exercicio():
    """Deleta um exercício informando seu `id` """
    id = request.args.get("id", type=int)
    session = Session()
    count = session.query(Exercicio).filter(Exercicio.id == id).delete()
    session.commit()

    if count:
        return {"mesage": "Exercicio removido", "id": id}, 200
    else:
        return {"mesage": "Exercicio não encontrado"}, 404

@app.put('/exercicio', tags=[exercicio_tag],
         responses={"200": ExercicioViewSchema, "400": ErrorSchema})
def editar_exercicio():
    """Edita um exercício existente"""
    try:
        id = request.args.get("id", type=int)
        session = Session()
        exercicio = session.query(Exercicio).filter(Exercicio.id == id).first()

        if not exercicio:
            return {"mesage": "Exercicio não encontrado"}, 404

        exercicio.titulo = request.form['titulo']
        exercicio.musculo = request.form['musculo']
        exercicio.descricao = request.form['descricao']

        if 'imagem' in request.files:
            imagem = request.files['imagem']
            filename = secure_filename(imagem.filename)
            imagem_path = os.path.join(UPLOAD_FOLDER, filename)
            imagem.save(imagem_path)
            exercicio.thumbnail = f"{UPLOAD_FOLDER}/{filename}"

        session.commit()
        return apresenta_exercicio(exercicio), 200

    except Exception as e:
        logger.error(f"Erro ao editar exercício: {e}")
        return {"mesage": f"Erro ao editar exercício: {str(e)}"}, 400

@app.post('/exercicio', tags=[exercicio_tag],
          responses={"200": ExercicioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_exercicio(form: ExercicioSchema):
    """Adiciona um novo exercício via """
    exercicio = Exercicio(
        titulo=form.titulo,
        musculo=form.musculo,
        descricao=form.descricao,
        thumbnail=form.thumbnail
    )
    try:
        session = Session()
        session.add(exercicio)
        session.commit()
        return apresenta_exercicio(exercicio), 200

    except IntegrityError:
        return {"mesage": "Exercício com mesmo título já existe."}, 409

    except Exception as e:
        logger.error(f"Erro ao salvar exercício: {e}")
        return {"mesage": "Erro ao salvar exercício."}, 400

@app.get('/exercicios', tags=[exercicio_tag],
         responses={"200": ListagemExerciciosSchema, "404": ErrorSchema})
def get_exercicios():
    """Lista todos os exercícios cadastrados"""
    session = Session()
    exercicios = session.query(Exercicio).all()
    if not exercicios:
        return {"exercicios": []}, 200
    return apresenta_exercicios(exercicios), 200

# ----------------- TREINO ------------------

@app.get('/treinos', tags=[treino_tag],
         responses={"200": ListagemTreinosSchema, "404": ErrorSchema})
def get_treinos():
    """Lista todos os treinos cadastrados"""
    session = Session()
    treinos = session.query(Treino).all()
    if not treinos:
        return {"treinos": []}, 200
    return apresenta_treinos(treinos), 200

@app.post('/treino', tags=[treino_tag],
          responses={"200": TreinoViewSchema, "400": ErrorSchema})
def add_treino(body: TreinoSchema):
    """Adiciona um novo treino com uma lista de exercícios"""
    logger.debug(f"Adicionando treino: {body.titulo}")
    session = Session()

    treino = Treino(titulo=body.titulo)

    for item in body.exercicios:
        treino_exercicio = TreinoExercicio(
            exercicio_id=item.exercicio_id,
            sets=item.sets,
            reps=item.reps
        )
        treino.exercicios_associados.append(treino_exercicio)

    try:
        session.add(treino)
        session.commit()
        return apresenta_treino(treino), 200
    except Exception as e:
        logger.error(f"Erro ao criar treino: {e}")
        return {"mesage": f"Erro ao criar treino: {str(e)}"}, 400

# --------------- EXERCÍCIOS INICIAIS -------------

def criar_exercicios_iniciais():
    session = Session()
    if session.query(Exercicio).count() == 0:
        exercicios_padrao = [
            Exercicio(titulo="Agachamento", musculo="Pernas", descricao="Fortalece as pernas", thumbnail="img/agachamento.png"),
            Exercicio(titulo="Supino reto", musculo="Peito", descricao="Trabalha o peitoral", thumbnail="img/supino.png"),
            Exercicio(titulo="Remada curvada", musculo="Costas", descricao="Fortalece dorsais", thumbnail="img/remada.png"),
            Exercicio(titulo="Rosca direta", musculo="Bíceps", descricao="Trabalha o bíceps", thumbnail="img/rosca.png"),
        ]

        session.add_all(exercicios_padrao)
        session.commit()
    session.close()

criar_exercicios_iniciais()
