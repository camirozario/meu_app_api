from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

from model import Session
from model.treino_exercicio import TreinoExercicio
from model.treino import Treino
from model.exercicio import Exercicio
from logger import logger

# client externo (ExerciseDB v1)
# services/exercisedb_open.py deve existir conforme combinamos
from services import exercisedb_open as ext_open

# schemas (mantidos do seu projeto)
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

load_dotenv()

# Pasta uploads
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Info API
info = Info(
    title="🏋️ Workout Builder API",
    version="1.0.0",
    description="""
## 📘️ API para Treinos e Exercícios

- CRUD de **exercícios pessoais** (DB)
- Catálogo **externo** ExerciseDB v1 (somente leitura)
- **Merge** (pessoais + externos) com **paginação**
- **Treinos** (sets/reps)
"""
)

app = OpenAPI(__name__, info=info)
CORS(app)

# Tags
home_tag = Tag(name="Documentação", description="Swagger UI em /openapi")
exercicio_tag = Tag(name="Exercicio", description="Exercícios pessoais (DB) e catálogo externo")
treino_tag = Tag(name="Treino", description="Operações para treinos")

# ---------------- HOME ----------------
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

# ---------------- EXERCÍCIOS PESSOAIS (DB) ----------------
@app.post('/upload_exercicio', tags=[exercicio_tag],
          responses={"200": ExercicioViewSchema, "400": ErrorSchema})
def upload_exercicio():
    """Cria exercício pessoal com upload de imagem"""
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
        return {"mesage": f"Erro ao salvar exercício: {e}"}, 400


@app.delete('/exercicio', tags=[exercicio_tag],
            responses={"200": ExercicioDelSchema, "404": ErrorSchema})
def delete_exercicio():
    """Remove exercício pessoal por id"""
    id = request.args.get("id", type=int)
    session = Session()
    count = session.query(Exercicio).filter(Exercicio.id == id).delete()
    session.commit()
    if count:
        return {"mesage": "Exercicio removido", "id": id}, 200
        # (mantive "mesage" conforme seu schema)
    else:
        return {"mesage": "Exercicio não encontrado"}, 404


@app.put('/exercicio', tags=[exercicio_tag],
         responses={"200": ExercicioViewSchema, "400": ErrorSchema})
def editar_exercicio():
    """Edita exercício pessoal (campos e imagem opcional)"""
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
        return {"mesage": f"Erro ao editar exercício: {e}"}, 400


@app.post('/exercicio', tags=[exercicio_tag],
          responses={"200": ExercicioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_exercicio(body: ExercicioSchema):  # <-- change 'form' -> 'body'
    """Adiciona um novo exercício via JSON"""
    exercicio = Exercicio(
        titulo=body.titulo,
        musculo=body.musculo,
        descricao=body.descricao,
        thumbnail=body.thumbnail
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
         responses={"200": ListagemExerciciosSchema})
def get_exercicios():
    """Lista apenas exercícios pessoais (DB)"""
    session = Session()
    exercicios = session.query(Exercicio).all()
    return apresenta_exercicios(exercicios), 200

# ---------------- EXTERNOS (ExerciseDB v1 - read only) ----------------
@app.get("/exercicios/default", tags=[exercicio_tag])
def exercicios_default():
    """
    Proxy do catálogo externo (sem salvar no banco).
    Query: bodyPart | target | equipment | limit | offset
    """
    import requests
    body_part = request.args.get("bodyPart")
    target = request.args.get("target")
    equipment = request.args.get("equipment")
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)

    try:
        if body_part:
            items, meta = ext_open.by_body_part(body_part, limit=limit, offset=offset)
        elif target:
            items, meta = ext_open.by_target(target, limit=limit, offset=offset)
        elif equipment:
            items, meta = ext_open.by_equipment(equipment, limit=limit, offset=offset)
        else:
            items, meta = ext_open.list_all(limit=limit, offset=offset)

        return {"count": len(items), "metadata": meta, "items": items}, 200

    except requests.HTTPError as e:
        return {"error": "external_http_error",
                "status": e.response.status_code,
                "text": e.response.text[:400]}, 502
    except Exception as e:
        return {"error": "external_request_failed", "detail": repr(e)}, 502


# ---------------- MERGE (pessoais + externos) COM PAGINAÇÃO ----------------
@app.get("/exercicios/todos", tags=[exercicio_tag])
def exercicios_todos():
    """
    Retorna pessoais (DB) + externos (ExerciseDB).
    Filtros extern: bodyPart | target | equipment | limit_ext
    Busca local: q
    Paginação final (merge): page | per_page
    """
    import requests

    # filtros para externos + busca local
    q = (request.args.get("q") or "").strip().lower()
    body_part = request.args.get("bodyPart")
    target = request.args.get("target")
    equipment = request.args.get("equipment")
    limit_ext = request.args.get("limit_ext", default=100, type=int)

    # paginação final
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=20, type=int)

    # --- pessoais (DB)
    session = Session()
    db_items = session.query(Exercicio).all()
    session.close()

    pessoais = [{
        "id": e.id,
        "titulo": e.titulo,
        "musculo": e.musculo,
        "descricao": e.descricao,
        "thumbnail": e.thumbnail,  # ex: "static/uploads/xxx.png"
        "source": "personal"
    } for e in db_items]

    if q:
        pessoais = [x for x in pessoais if q in (x["titulo"] or "").lower()]

    # --- externos (API)
    try:
        if body_part:
            ext_list, _ = ext_open.by_body_part(body_part, limit=limit_ext, offset=0)
        elif target:
            ext_list, _ = ext_open.by_target(target, limit=limit_ext, offset=0)
        elif equipment:
            ext_list, _ = ext_open.by_equipment(equipment, limit=limit_ext, offset=0)
        else:
            ext_list, _ = ext_open.list_all(limit=limit_ext, offset=0)
    except Exception as e:
        logger.error(f"External API error: {e}")
        ext_list = []

    def norm(x):
        # v1 fields: name, gifUrl, imageUrl, targetMuscles[], bodyParts[], instructions[]
        titulo = (x.get("name") or "").strip()
        if not titulo:
            return None
        if q and q not in titulo.lower():
            return None

        musc = None
        tms = x.get("targetMuscles") or []
        if isinstance(tms, list) and tms:
            musc = tms[0]
        else:
            bps = x.get("bodyParts") or []
            musc = bps[0] if isinstance(bps, list) and bps else None

        instr = x.get("instructions")
        if isinstance(instr, list):
            instr = " ".join(step for step in instr if isinstance(step, str))
        if isinstance(instr, str):
            instr = instr.strip()

        thumb = x.get("imageUrl") or x.get("gifUrl")

        return {
            "id": None,  # externo não tem id local
            "titulo": titulo,
            "musculo": musc,
            "descricao": (instr[:255] if instr else None),
            "thumbnail": thumb,
            "source": "external"
        }

    externos = [m for m in (norm(x) for x in ext_list) if m]

    # --- merge & paginação
    all_items = pessoais + externos
    total = len(all_items)
    if per_page < 1:
        per_page = 20
    if page < 1:
        page = 1
    start = (page - 1) * per_page
    end = start + per_page
    page_items = all_items[start:end]
    pages = (total + per_page - 1) // per_page

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": pages,
        "items": page_items
    }, 200


# ---------------- HEALTHCHECK EXTERNO ----------------
@app.get("/health/external", tags=[exercicio_tag])
def health_external():
    try:
        data = ext_open.body_parts_list()
        return {"ok": True, "count": len(data), "sample": data[:5]}, 200
    except Exception as e:
        return {"ok": False, "error": repr(e)}, 502


# ---------------- TREINOS ----------------
@app.get('/treinos', tags=[treino_tag],
         responses={"200": ListagemTreinosSchema})
def get_treinos():
    session = Session()
    treinos = session.query(Treino).all()
    return apresenta_treinos(treinos), 200


@app.post('/treino', tags=[treino_tag],
          responses={"200": TreinoViewSchema, "400": ErrorSchema})
def add_treino(body: TreinoSchema):
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
        return {"mesage": f"Erro ao criar treino: {e}"}, 400


# ---------------- SEED INICIAL ----------------
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
