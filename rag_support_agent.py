import os
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# === CONFIGURAÇÃO DA CHAVE GROQ (2 OPÇÕES) ===
# Opção 1: Cole sua chave aqui (só pra teste local)
os.environ["GROQ_API_KEY"] = "CHAVE API GROQ"  # ← SUBSTITUA

# Opção 2: (RECOMENDADO) Use st.secrets no Streamlit (deixe comentado por enquanto)
# import streamlit as st
# if "GROQ_API_KEY" not in os.environ:
#     os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Configurações
DB_PATH = "./chroma_db"
GROQ_MODEL = "llama-3.1-8b-instant"  # Rápido, barato e 100% funcional em nov/2025

# Base de conhecimento
KNOWLEDGE_BASE = [
    "Para redefinir sua senha, acesse o site, clique em 'Esqueci minha senha' e siga as instruções enviadas por e-mail.",
    "O prazo de entrega padrão é de 3 a 7 dias úteis após a confirmação do pagamento.",
    "Aceitamos cartão de crédito, boleto bancário e Pix como formas de pagamento.",
    "Para cancelar um pedido, entre em contato pelo chat ou e-mail em até 2 horas após a compra.",
    "Nossa garantia é de 90 dias para defeitos de fabricação. Entre em contato com o suporte anexando fotos do produto.",
    "O rastreio do pedido é enviado por e-mail assim que o produto for despachado.",
    "Trabalhamos de segunda a sexta das 9h às 18h. Aos finais de semana o suporte é via e-mail.",
    "Para trocar um produto, acesse Minha Conta > Pedidos > Solicitar Troca/Devolução.",
    "O reembolso é processado em até 10 dias úteis após o recebimento do produto devolvido.",
    "Sim, fazemos entrega para todo o Brasil, inclusive interior e capitais."
]

def create_or_load_vectorstore():
    embedding = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    if os.path.exists(DB_PATH):
        return Chroma(persist_directory=DB_PATH, embedding_function=embedding)
    else:
        print("Criando base de conhecimento...")
        vectorstore = Chroma.from_texts(
            texts=KNOWLEDGE_BASE,
            embedding=embedding,
            persist_directory=DB_PATH
        )
        print("Base criada!")
        return vectorstore

def create_rag_chain():
    vectorstore = create_or_load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    llm = ChatGroq(model=GROQ_MODEL, temperature=0.3, max_tokens=1024)
    
    prompt = ChatPromptTemplate.from_template("""
Você é um assistente de suporte ao cliente brasileiro, educado e profissional.
Use apenas o contexto abaixo. Se não souber, diga que vai encaminhar para um humano.

Contexto:
{context}

Pergunta: {question}

Resposta:""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain