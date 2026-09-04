# ClaudeMind AI

Chatbot web com frontend estatico e API serverless em Python. A resposta e gerada pela API da Groq.

## Deploy na Vercel

1. Suba este repositorio no GitHub e importe-o em [vercel.com](https://vercel.com).
2. Em **Settings > Environment Variables**, adicione:

   - `GROQ_API_KEY`: sua chave secreta da Groq.
   - `GROQ_MODEL`: opcional. Padrao: `llama-3.1-8b-instant`. Use um modelo atualmente disponivel na sua conta Groq.

3. Faca o deploy. O arquivo `vercel.json` direciona `/api/chat` para a funcao Python.

O plano gratuito da Vercel e suficiente para um projeto pessoal, mas a funcao possui limites de execucao e uso. A API da Groq tambem tem limites proprios, que podem mudar conforme a conta e o modelo.

## Desenvolvimento local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:GROQ_API_KEY="sua-chave-da-groq"
python api/index.py
```

Abra `http://localhost:3000` no navegador.

## Estrutura

- `public/`: interface do chat, sem segredo no navegador.
- `api/index.py`: endpoint serverless que chama a Groq.
- `vercel.json`: configuracao de build e rotas.
