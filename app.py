import streamlit as st
from rag_support_agent import create_rag_chain

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Suporte Inteligente",
    page_icon="robot",
    layout="centered"
)

# ==================== FORÇA CORES LEGÍVEIS (CLARO E ESCURO) ====================
st.markdown("""
<style>
    /* Fundo geral */
    .main {background-color: #ffffff;}
    
    /* Mensagens do usuário */
    .user-message {
        background-color: #e3f2fd;
        color: #0d47a1 !important;
        padding: 12px 16px;
        border-radius: 20px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 15px;
        font-size: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Mensagens do assistente */
    .assistant-message {
        background-color: #f5f5f5;
        color: #1a1a1a !important;
        padding: 12px 16px;
        border-radius: 20px;
        max-width: 80%;
        margin-right: auto;
        margin-bottom: 15px;
        font-size: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Garante que o texto dentro do chat seja sempre legível */
    .stChatMessage * {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== TÍTULO ====================
st.title("Suporte ao Cliente 24h")
st.markdown("**Fale com nosso assistente virtual a qualquer hora**")

# ==================== INICIALIZAÇÃO ====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Como posso te ajudar hoje?"}
    ]

if "rag_chain" not in st.session_state:
    with st.spinner("Carregando o assistente... (só na primeira vez)"):
        st.session_state.rag_chain = create_rag_chain()
    st.success("Assistente pronto!")

# ==================== EXIBE HISTÓRICO ====================
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT DO USUÁRIO ====================
if prompt := st.chat_input("Digite sua dúvida aqui..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

    # Responde
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta = st.session_state.rag_chain.invoke(prompt)
                st.markdown(f'<div class="assistant-message">{resposta}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                erro = "Desculpe, ocorreu um erro. Tente novamente em alguns segundos."
                st.markdown(f'<div class="assistant-message">{erro}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": erro})

# ==================== RODAPÉ ====================
st.markdown("---")
st.caption("Suporte com Inteligência Artificial • Baseado na base de conhecimento da loja")