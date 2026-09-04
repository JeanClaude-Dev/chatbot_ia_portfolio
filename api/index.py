import json
import http.client
import os

from flask import Flask, jsonify, request, send_from_directory

PUBLIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))
app = Flask(__name__, static_folder=None)

SYSTEM_PROMPT = (
    "Voce e um assistente de inteligencia artificial avancado que responde "
    "perguntas de forma clara e util."
)
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"


@app.get("/")
def home():
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.get("/api/health")
def health():
    api_key = (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEY") or "").strip()
    return jsonify({
        "version": "1983428",
        "provider": "openrouter",
        "model": OPENROUTER_MODEL,
        "key_configured": bool(api_key),
    })


@app.post("/api/chat")
@app.post("/<path:path>")
def chat(path=None):
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
        api_key = (
            os.environ.get("OPENROUTER_API_KEY")
            or os.environ.get("OPENROUTER_KEY")
            or ""
        ).strip().strip('"\'')
        if not api_key:
            raise RuntimeError(
                "Cadastre OPENROUTER_API_KEY em Settings > Environment Variables na Vercel "
                "e faca um novo Redeploy."
            )

        body = json.dumps(
            {
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + clean_messages,
                "temperature": 0.7,
            }
        ).encode("utf-8")
        connection = http.client.HTTPSConnection("openrouter.ai", timeout=30)
        connection.request(
            "POST",
            "/api/v1/chat/completions",
            body=body,
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
                "HTTP-Referer": "https://chatbot-ia-portfolio-nine.vercel.app",
                "X-Title": "ClaudeMind AI",
            },
        )
        response = connection.getresponse()
        response_data = json.loads(response.read().decode("utf-8"))
        if response.status >= 400:
            raise RuntimeError(json.dumps(response_data))
        text = response_data["choices"][0]["message"]["content"]
        return jsonify({"message": text})
    except Exception as error:
        return jsonify({"error": f"Erro ao consultar o OpenRouter: {error}"}), 502


@app.get("/<path:path>")
def static_files(path):
    requested_file = os.path.join(PUBLIC_DIR, path)
    if os.path.isfile(requested_file):
        return send_from_directory(PUBLIC_DIR, path)
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.errorhandler(404)
def handle_not_found(error):
    if request.method == "GET":
        return send_from_directory(PUBLIC_DIR, "index.html")
    return jsonify({"error": "Rota nao encontrada."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
