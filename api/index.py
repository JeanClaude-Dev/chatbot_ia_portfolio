import os

from flask import Flask, jsonify, request, send_from_directory
from groq import Groq

app = Flask(__name__, static_folder="../public", static_url_path="")

SYSTEM_PROMPT = (
    "Voce e um assistente de inteligencia artificial avancado que responde "
    "perguntas de forma clara e util."
)


def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("A variavel GROQ_API_KEY nao foi configurada.")
    return Groq(api_key=api_key)


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    messages = payload.get("messages")

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Envie ao menos uma mensagem."}), 400

    clean_messages = [
        {"role": message.get("role"), "content": message.get("content")}
        for message in messages
        if isinstance(message, dict)
        and message.get("role") in {"user", "assistant"}
        and isinstance(message.get("content"), str)
        and message.get("content", "").strip()
    ]

    if not clean_messages:
        return jsonify({"error": "Nao foi encontrada uma mensagem valida."}), 400

    try:
        response = get_client().chat.completions.create(
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + clean_messages,
            model=os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0.7,
        )
        text = response.choices[0].message.content or "Nao consegui gerar uma resposta."
        return jsonify({"message": text})
    except Exception as error:
        return jsonify({"error": f"Erro ao consultar a IA: {error}"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
