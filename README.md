# 🏋️ POWER PLAN API

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

1. Crie um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   flask --app app run --host 0.0.0.0 --port 5000
   ```

   A API ficará disponível em:  
👉 http://localhost:5000

A API está estruturada de forma a conectar-se com uma API externa. Como indicado na imagem abaixo
<img width="1017" height="508" alt="Screenshot 2025-09-28 232610" src="https://github.com/user-attachments/assets/3e758796-d41a-4c68-aee6-1dc71605fd7b" />


---

## 🐳 Executando com Docker

### Usando apenas Docker

1. Construa a imagem:
   ```
   docker build -t meu_app_api:dev .
   ```

2. Rode o container:
    ```
   docker run --rm -p 5000:5000 meu_app_api:dev
    ```

---

### Usando Docker Compose

1. Suba os containers:
   ```
   docker compose up --build
   ```

3. Volumes montados automaticamente:
   - database/ → banco SQLite  
   - static/uploads/ → imagens  
   - log/ → logs  
   - instance/ → configs extras do Flask  

---

## 🌐 API Externa Utilizada
https://v1.exercisedb.dev/
