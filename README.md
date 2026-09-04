# ClaudeMind AI

Chatbot web com frontend estatico e API serverless em Python. A resposta e gerada por um modelo Llama gratuito via OpenRouter.

## Deploy na Vercel

1. Suba este repositorio no GitHub e importe-o em [vercel.com](https://vercel.com).
2. Em **Settings > Environment Variables**, adicione:

   - `OPENROUTER_API_KEY`: sua chave gratuita do OpenRouter. Esta e a unica variavel necessaria.
   - Se voce cadastrou a chave com o nome `OPENROUTER_KEY`, o endpoint tambem aceita esse nome.

3. Faca o deploy. O arquivo `vercel.json` direciona `/api/chat` para a funcao Python.

O plano gratuito da Vercel e suficiente para um projeto pessoal, mas a funcao possui limites de execucao e uso. Os modelos gratuitos do OpenRouter tambem possuem limites de uso e disponibilidade.

## Desenvolvimento local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:OPENROUTER_API_KEY="sua-chave-do-openrouter"
python api/index.py
```

Abra `http://localhost:3000` no navegador.

## Estrutura

- `public/`: interface do chat, sem segredo no navegador.
- `api/index.py`: endpoint serverless que chama o OpenRouter com um modelo Llama.
- `vercel.json`: configuracao de build e rotas.
