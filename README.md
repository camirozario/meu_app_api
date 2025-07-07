# 🏋️ Workout Builder API

Uma API RESTful para gerenciamento de treinos personalizados, com suporte a exercícios com imagem, descrições e estrutura completa para criação e consulta de treinos. Foi feita como MVP para a pós de Desenvolvimento FullStack faculdade PUCRIO.
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
├── app.py # Arquivo principal com as rotas
├── model/ # Modelos do SQLAlchemy
│ ├── init.py
│ ├── base.py
│ ├── treino.py
│ ├── treino_exercicio.py
│ └── exercicio.py
├── schemas/ # Schemas Pydantic
│ ├── init.py
│ ├── treino.py
│ ├── exercicio.py
│ └── error.py
├── static/uploads/ # Imagens de exercícios
├── database/db.sqlite3 # Banco SQLite
├── logger.py
└── requirements.txt

yaml
Copy
Edit

---

## 📦 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/workout-builder-api.git
cd workout-builder-api
Crie um ambiente virtual:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
Instale as dependências:

bash
Copy
Edit
pip install -r requirements.txt
Execute a aplicação:

bash
Copy
Edit
flask --app app run --host 0.0.0.0 --port 5000