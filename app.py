import streamlit as st
from groq import Groq
from PIL import Image
import time

import base64
from io import BytesIO

# CONFIGURAÇÃO
st.set_page_config(
    page_title="ClaudeMind",
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

def banner_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ---------- TITULO ----------
banner = Image.open("banner.png")

st.markdown("""
<style>

.banner-container{
position:relative;
width:100%;
height:220px;
overflow:hidden;
border-radius:12px;
}

.banner-container img{
width:100%;
height:220px;
object-fit:cover;
}

.banner-text{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%, -50%);
font-size:48px;
font-weight:900;
color:white;
letter-spacing:2px;
text-shadow:0px 0px 20px rgba(0,0,0,0.8);
}

</style>
""", unsafe_allow_html=True)

banner = Image.open("banner.png")

st.markdown("""
<style>

.banner-container{
position:relative;
width:100%;
height:220px;
overflow:hidden;
border-radius:12px;
}

.banner-container img{
width:100%;
height:220px;
object-fit:cover;
}

.banner-text{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%, -50%);
font-size:48px;
font-weight:900;
color:white;
letter-spacing:2px;
text-shadow:0px 0px 20px rgba(0,0,0,0.8);
}

</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="banner-container">
<img src="data:image/png;base64,{banner_to_base64(banner)}">
<div class="banner-text">ClaudeMind</div>
</div>
""", unsafe_allow_html=True)


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
col1, col2 = st.columns([8,1])

with col2:
    if st.button("🗑️ Limpar"):
        st.session_state.messages = []
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