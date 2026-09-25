import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from google import genai
from google.genai.errors import ServerError, APIError
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Carregar variáveis de ambiente primeiro
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não foi configurada no ficheiro .env")

# 2. Inicialização dos Embeddings do Google Gemini
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

# 3. Inicialização do cliente Gemini SDK oficial
client = genai.Client(api_key=api_key)

# Inicialização do Banco Vetorial (ChromaDB)
CHROMA_PATH = "./chroma_db"

if os.path.exists(CHROMA_PATH):
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
else:
    vector_db = None

# 3. Inicialização do FastAPI
app = FastAPI(title="API Assistente RAG - Rafael Kottwitz")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Modelos de Dados
class Message(BaseModel):
    role: str
    content: str

class ChatPayload(BaseModel):
    pergunta: str
    historico: Optional[List[Message]] = []

def formatar_historico(historico: List[Message]) -> str:
    if not historico:
        return "Nenhum histórico anterior."
    
    ultimas_mensagens = historico[-4:]
    linhas = []
    for msg in ultimas_mensagens:
        papel = "Cliente" if msg.role.lower() == "user" else "Assistente"
        linhas.append(f"{papel}: {msg.content}")
    return "\n".join(linhas)

# 5. Endpoint Principal com Streaming
@app.post("/chat")
async def chat_endpoint(payload: ChatPayload):
    query = payload.pergunta.strip()
    if not query:
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

    historico_str = formatar_historico(payload.historico)
    
    # Recupera os 2 fragmentos mais relevantes do ChromaDB
    contexto = ""
    if vector_db:
        docs = vector_db.similarity_search(query, k=2)
        contexto = "\n\n".join([d.page_content for d in docs])

    # Prompt Consultivo com Escopo Ajustado
    prompt = f"""Você é o assistente virtual consultivo do desenvolvedor Rafael Batista Kottwitz.
Sua função é qualificar potenciais clientes, tirando dúvidas e recomendando soluções em desenvolvimento de software.

Escopo de Serviços Atendidos:
- Landing Pages e Sites Institucionais.
- Aplicativos móveis SIMPLES (apenas para Android, não desenvolve para iOS).
- E-commerces e Sistemas Corporativos PEQUENOS.
- Sistemas web relacionais com banco de dados (ex: PostgreSQL) e Automações/APIs.

DIRETRIZES DE OURO (OBRIGATÓRIO):
1. PREÇOS SEMPRE EXATOS: Quando o cliente perguntar o valor de qualquer serviço (ex: "Você faz app para Android?"), DEVES informar imediatamente e sem rodeios a faixa de preço exata descrita na base de conhecimento. Para o aplicativo Android, o valor é obrigatoriamente **R$ 2.000 a R$ 5.000**. É estritamente proibido citar valores antigos (como 3k a 8k), omitir preços ou responder com "valores sob consulta".
2. ESCOPO DE ATUAÇÃO: O Rafael atua de forma autônoma. NÃO desenvolve para iOS (iPhone/iPad) nem projetos gigantescos ou de altíssima complexidade. Se solicitarem iOS, recusa educadamente e sugere o WhatsApp (47) 98825-8610.
3. CONCISÃO E TOM: Responde de forma direta, acolhedora e humana (máximo 2 a 3 frases). Termina sempre com uma pergunta simples para engajar o cliente na ideia do projeto dele.
4. NUNCA INVENTE DADOS: Utiliza estritamente os valores, prazos e descrições presentes na base de conhecimento abaixo.

Base de Conhecimento:
{contexto}

Histórico da Conversa:
{historico_str}

Pergunta do Cliente: {query}
"""

    def stream_generator():
        try:
            # Chamada de streaming usando genai.Client
            response = client.models.generate_content_stream(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except ServerError:
            yield "\n\n⚠️ *Serviço temporariamente indisponível. Tente novamente em instantes ou fale no WhatsApp: (47) 98825-8610.*"
        except APIError as e:
            if "429" in str(e):
                yield "\n\n⚠️ *Atingimos o limite temporário de requisições. Aguarde alguns segundos ou mande mensagem no WhatsApp: (47) 98825-8610.*"
            else:
                yield f"\n\n⚠️ *Erro na API do Gemini. Fale diretamente no WhatsApp: (47) 98825-8610.*"
        except Exception as e:
            yield f"\n\n⚠️ *Erro ao processar a resposta. Contato via WhatsApp: (47) 98825-8610.*"

    return StreamingResponse(stream_generator(), media_type="text/plain")

# 6. Healthcheck
@app.get("/health")
def health_check():
    return {
        "status": "online",
        "vector_db": vector_db is not None,
        "gemini_configured": bool(api_key),
        "model": "gemini-3.5-flash-lite"
    }