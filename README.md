# Portfolio & Assistente RAG IA | Rafael Kottwitz

<p align="center">
  <b>Portfólio profissional de alta performance com inteligência artificial integrada para atendimento consultivo.</b>
</p>

<p align="center">
  <a href="https://portfolio-venda.onrender.com" target="_blank">🌐 Ver Backend API</a> •
  <a href="https://festivalsushi.netlify.app/" target="_blank">🚀 Ver Exemplo de Landing Page</a>
</p>

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi desenvolvido com uma arquitetura moderna separada em **Frontend** e **Backend**, otimizada para alta velocidade de carregamento, design minimalista (Dark Mode com acentos neon) e baixo consumo de recursos.

### **Frontend (`frontend-portfolio`)**
* **HTML5 & CSS3**: Design responsivo com efeitos de *Glassmorphism*, imagens imersivas de fundo e adaptação fluida para dispositivos móveis (`dvh`).
* **JavaScript (Vanilla)**: Lógica de comunicação assíncrona (`fetch`) com *Streaming* de respostas da IA em tempo real.
* **Hospedagem**: Vercel.

### **Backend & Inteligência Artificial (`Back-end-bot`)**
* **FastAPI**: Framework Python de alta performance para a API assíncrona.
* **Google Gemini API (`google-genai` & `GoogleGenerativeAIEmbeddings`)**: Utilizado para geração de texto e vetorização eficiente, substituindo modelos locais pesados e garantindo compatibilidade com o limite de memória do plano gratuito.
* **ChromaDB**: Base de dados vetorial leve para armazenamento de contexto RAG (*Retrieval-Augmented Generation*).
* **Hospedagem**: Render.

---

## 📂 Estrutura do Repositório

```text
├── Back-end-bot/
│   ├── chroma_db/             # Base de dados vetorial local / ChromaDB
│   ├── api.py                 # Aplicação principal FastAPI e endpoints de chat
│   ├── ingest.py              # Script de ingestão e vetorização de documentos
│   ├── requirements.txt       # Dependências otimizadas do Python
│   └── .env                   # Variáveis de ambiente (Chaves de API)
│
└── frontend-portfolio/
    ├── index.html             # Página principal do portfólio
    ├── styles.css             # Estilização moderna, tema escuro e responsividade
    └── script.js              # Lógica do widget de chat e streaming de respostas
