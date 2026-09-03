# ClaudeMind AI – Intelligent Chatbot


ClaudeMind AI é um **chatbot inteligente** desenvolvido em Python com **Streamlit**, utilizando a **API da Groq**. O modelo pode ser definido nos secrets do Streamlit.

---

## 🌟 Funcionalidades

- Interface moderna e futurista em **modo dark**  
- Chat com respostas da IA em **tempo real** (efeito digitação)  
- Histórico de conversa durante a sessão  
- Botão para **limpar conversa**  
- Nome e branding integrados ao banner (**ClaudeMind**)  
- Fácil deploy em **Streamlit Cloud ou outras plataformas**  

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**  
- **[Streamlit](https://streamlit.io/)** – framework web para aplicações interativas  
- **[Groq API](https://www.groq.com/)** – plataforma de inferência de IA  
- **Llama 3.3 70B** – modelo de linguagem avançado  
- **Pillow** – manipulação de imagens (banner)  

---

## Configuração

Configure os secrets do Streamlit:

```toml
GROQ_API_KEY = "sua-chave-da-groq"
GROQ_MODEL = "llama-3.3-70b-versatile"
```

Se `GROQ_MODEL` não for definido, o app usa `llama-3.1-8b-instant`, que é o padrão compatível com a configuração anterior.

