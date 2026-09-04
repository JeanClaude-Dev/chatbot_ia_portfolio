import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

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

        api_url = "https://openrouter.ai/api/v1/chat/completions"
        body = json.dumps(
            {
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + clean_messages,
                "temperature": 0.7,
            }
        ).encode("utf-8")
        response_request = Request(api_url, data=body, method="POST")
        response_request.add_header("Authorization", f"Bearer {api_key}")
        response_request.add_header("Content-Type", "application/json")
        response_request.add_header(
            "HTTP-Referer", "https://chatbot-ia-portfolio-nine.vercel.app"
        )
        response_request.add_header("X-Title", "ClaudeMind AI")
        with urlopen(response_request, timeout=30) as response:
            response_data = json.loads(response.read().decode("utf-8"))
        text = response_data["choices"][0]["message"]["content"]
        return jsonify({"message": text})
    except HTTPError as error:
        details = error.read().decode("utf-8")
        return jsonify({"error": f"Erro ao consultar o OpenRouter: {details}"}), 502
    except URLError as error:
        return jsonify({"error": f"Nao foi possivel conectar ao OpenRouter: {error.reason}"}), 502
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
