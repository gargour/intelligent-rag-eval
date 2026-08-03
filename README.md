.env Structure :
GROK\_API\_KEY=
GROK\_MODEL=llama-3.3-70b-versatile
GROK\_BASE\_URL=https://api.groq.com/openai/v1
LLM\_PROVIDER=grok

OPENAI\_API\_KEY=
EMBEDDING\_PROVIDER=sentence-transformers
EMBEDDING\_MODEL=text-embedding-3-small

VECTORSTORE\_PROVIDER=faiss
FAISS\_INDEX\_DIR=./data/faiss\_index

DATABASE\_URL=postgresql://raguser:ragpass@localhost:5432/ragdb

API\_HOST=0.0.0.0
API\_PORT=8000
API\_SECRET\_KEY=change-me
API\_BASE\_URL=http://localhost:8000



\# 🤖 AI Research Assistant — RAG + LLM Evaluation + Agentic System



Assistant IA de recherche documentaire complet : ingestion multi-format, recherche sémantique avec citations, requêtes multi-modes, évaluation rigoureuse (RAGAS), et agent intelligent — le tout conteneurisé avec CI/CD automatisé.



\## 🎯 Fonctionnalités



\- \*\*Upload\*\* PDF, DOCX, TXT avec extraction et chunking automatique

\- \*\*Q\&A avec citations\*\* — réponses sourcées avec numéro de page et extrait exact

\- \*\*Compare Documents\*\* — comparaison structurée entre deux documents

\- \*\*Generate Report\*\* — génération de rapports thématiques

\- \*\*Agent intelligent\*\* (`/chat/smart`) — un LLM décide automatiquement quelle action effectuer (qa/résumé/comparaison/rapport) selon la question posée, sans sélection manuelle

\- \*\*Évaluation RAG\*\* — RAGAS officiel (faithfulness, answer relevancy, context precision/recall) + LLM-judge maison

\- \*\*Reranking\*\* — cross-encoder pour affiner la pertinence des résultats FAISS



\## 🏗️ Stack technique



| Composant | Technologie |

|---|---|

| Backend | FastAPI |

| Frontend | Streamlit |

| LLM | Groq (Llama 3.3 70B) |

| Embeddings | sentence-transformers (local) |

| Vector store | FAISS |

| Base de données | PostgreSQL |

| Évaluation | RAGAS 0.2.x |

| Déploiement | Docker + Docker Compose |

| CI/CD | GitHub Actions |



\## 🚀 Démarrage rapide (Docker)



```bash

git clone <repo-url>

cd ai-research-assistant

cp .env.example .env  # ajouter tes clés API

docker-compose up -d --build

```



\- Frontend : http://localhost:8501

\- API/Swagger : http://localhost:8000/docs



\## 📊 Résultats d'évaluation RAGAS



| Métrique | Score |

|---|---|

| Faithfulness | 0.85 |

| Answer Relevancy | 0.91 |

| Context Precision | 0.88 |

| Context Recall | 1.00 |



\## 🧪 Tests



```bash

pytest -v

```

7/7 tests passent.



\## 🔄 CI/CD



Chaque push sur `main` déclenche automatiquement :

\- \*\*CI\*\* : exécution des tests (`pytest`)

\- \*\*CD\*\* : build et push des images Docker vers Docker Hub



\## 📁 Structure du projet

app/ # Backend FastAPI (routes, RAG, agents, évaluation)

frontend/ # Interface Streamlit (5 pages)

tests/ # Tests unitaires et d'intégration

.github/ # Workflows CI/CD

docker/ # Dockerfiles





\## 📝 Licence



Realise Par Amr GARA 

© 2026 Gara Industries

Projet académique — Data Science \& IA.

