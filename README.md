# 🏋️ Workout Builder API

Uma API RESTful para gerenciamento de treinos personalizados, com suporte a exercícios com imagem, descrições e estrutura completa para criação e consulta de treinos.  
Foi desenvolvida como MVP para a pós-graduação em **Desenvolvimento FullStack - PUC-Rio**.

---

## 🚀 Funcionalidades

- ✅ Adicionar, listar, editar e excluir **exercícios**
- 🖼️ Upload de imagem (thumbnail) para os exercícios
- 🏋️ Criar treinos personalizados com múltiplos exercícios, sets e reps
- 📘 Documentação interativa gerada com **Swagger UI** (`/openapi/swagger`)
- 🔒 CORS habilitado para integração com front-end
- 🔧 Base em **Flask**, **SQLAlchemy**, **Pydantic** e **Flask-OpenAPI3**

---

## 📂 Estrutura do Projeto

meu_app_api/
│
├── app.py                  # Arquivo principal com as rotas
├── model/                  # Modelos do SQLAlchemy
│   ├── __init__.py
│   ├── base.py
│   ├── treino.py
│   ├── treino_exercicio.py
│   └── exercicio.py
├── schemas/                # Schemas Pydantic
│   ├── __init__.py
│   ├── treino.py
│   ├── exercicio.py
│   └── error.py
├── static/uploads/         # Imagens de exercícios
├── database/db.sqlite3     # Banco SQLite
├── logger.py
└── requirements.txt

---

## 📦 Instalação Manual

1. Clone este repositório:
   git clone https://github.com/seu-usuario/workout-builder-api.git
   cd workout-builder-api

2. Crie um ambiente virtual:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. Instale as dependências:
   pip install -r requirements.txt

4. Execute a aplicação:
   flask --app app run --host 0.0.0.0 --port 5000

A API ficará disponível em:  
👉 http://localhost:5000

---

## 🐳 Executando com Docker

### Usando apenas Docker

1. Construa a imagem:
   docker build -t meu_app_api:dev .

2. Rode o container:
   docker run --rm -p 5000:5000 meu_app_api:dev

---

### Usando Docker Compose

1. Suba os containers:
   docker compose up --build

2. Volumes montados automaticamente:
   - database/ → banco SQLite  
   - static/uploads/ → imagens  
   - log/ → logs  
   - instance/ → configs extras do Flask  

---

## 🌐 Endpoints principais

- Swagger UI → http://localhost:5000/openapi/swagger  
- ReDoc → http://localhost:5000/openapi/redoc  
- RapiDoc → http://localhost:5000/openapi/rapidoc  
- Exercícios → GET /exercicios  
- Treinos → GET /treinos