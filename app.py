import streamlit as st
from groq import Groq
from PIL import Image
import time

# CONFIGURAÇÃO
st.set_page_config(
    page_title="OPEERA AI",
    page_icon="🤖",
    layout="wide"
)

# ---------- CSS FUTURISTA ----------
st.markdown("""
<style>

body{
background: linear-gradient(135deg,#0b0f1a,#05070f);
}

.main-title{
text-align:center;
font-size:52px;
font-weight:900;
color:#07b458;
margin-top:10px;
}

.subtitle{
text-align:center;
color:#9ca3af;
font-size:18px;
margin-bottom:30px;
}

.chat-box{
background:#0f172a;
padding:20px;
border-radius:15px;
border:1px solid #1f2937;
}

[data-testid="stChatMessageUser"]{
background:#020617;
border-radius:12px;
padding:10px;
}

[data-testid="stChatMessageAssistant"]{
background:#071a12;
border-radius:12px;
padding:10px;
border:1px solid #07b458;
}

button{
background-color:#07b458 !important;
color:white !important;
border-radius:8px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- BANNER ----------
banner = Image.open("banner.png")
st.image(banner, use_container_width=True)

# ---------- TITULO ----------
st.markdown('<div class="main-title">OPEERA AI</div>', unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">Plataforma de inteligência artificial para perguntas e respostas</div>',
unsafe_allow_html=True
)

st.divider()

# ---------- GROQ ----------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Configure a chave GROQ_API_KEY no secrets.")
    st.stop()

# ---------- HISTÓRICO ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- BOTÃO LIMPAR ----------
col1,col2,col3 = st.columns([1,1,1])

with col2:
    if st.button("🗑️ Limpar conversa"):
        st.session_state.messages=[]
        st.rerun()

# ---------- CHAT ----------
for message in st.session_state.messages:

    avatar="👤" if message["role"]=="user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------- INPUT ----------
if prompt := st.chat_input("Digite qualquer pergunta..."):

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        placeholder = st.empty()

        with st.spinner("Pensando..."):

            try:

                system_prompt={
                    "role":"system",
                    "content":
                    "Você é um assistente de inteligência artificial avançado que responde perguntas de forma clara e útil."
                }

                mensagens=[system_prompt]+st.session_state.messages

                resposta = client.chat.completions.create(
                    messages=mensagens,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7
                )

                texto = resposta.choices[0].message.content

                resposta_parcial=""

                # efeito digitação
                for palavra in texto.split():
                    resposta_parcial += palavra + " "
                    placeholder.markdown(resposta_parcial)
                    time.sleep(0.02)

                st.session_state.messages.append({
                    "role":"assistant",
                    "content":texto
                })

            except Exception as e:
                st.error(f"Erro: {e}")