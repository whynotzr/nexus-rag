<div align="center">

# 🧠 NEXUS-RAG
### Moteur IA d'Analyse Documentaire & Recherche Vectorielle (FastAPI • ChromaDB • SSE)

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-Async-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/ChromaDB-Vector_Store-A855F7?style=for-the-badge" alt="ChromaDB" />
<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />

</div>

---

## ✨ Architecture
* **Chunking intelligent** avec fenêtre glissante (`overlap`) pour préserver le contexte sémantique.
* **Indexation vectorielle persistante** avec **ChromaDB**.
* **Endpoints REST & Streaming SSE** (`/api/v1/ingest`, `/api/v1/query`, `/api/v1/query/stream`) avec citations exactes des sources et scores de pertinence.
* **Validation Pydantic v2**, suite de tests `pytest` et conteneurisation Docker.

## 🚀 Lancement
```bash
git clone https://github.com/whynotzr/nexus-rag.git
cd nexus-rag
cp .env.example .env
docker compose up --build
```
La documentation interactive OpenAPI (Swagger) est accessible sur `http://localhost:8000/docs`.
