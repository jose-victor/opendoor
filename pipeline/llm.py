#!/usr/bin/env python3
"""Cliente mínimo para executar prompts via Gemini API ou Ollama."""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"
DEFAULT_OLLAMA_MODEL = "gemma4:e4b"
REQUEST_TIMEOUT = 60
RETRY_STATUS = {429, 500, 503}  # limite do plano grátis e instabilidade: tenta de novo com espera crescente


def _load_env(path=ROOT / ".env"):
    """Lê o .env da raiz (formato CHAVE=valor) sem sobrescrever o que já está no ambiente."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _post_json(url, payload, headers=None, tries=4):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in RETRY_STATUS and tries > 1:
            time.sleep(int(exc.headers.get("Retry-After") or 0) or 2 ** (5 - tries) * 5)
            return _post_json(url, payload, headers, tries - 1)
        detail = exc.read().decode("utf-8", "replace")[:300]  # a mensagem do Google diz se foi limite, modelo, chave...
        raise RuntimeError(f"A API do modelo respondeu com HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Não foi possível conectar à API do modelo: {exc.reason}.") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("A API do modelo retornou uma resposta JSON inválida.") from exc


def _generate_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Defina GEMINI_API_KEY para usar o backend Gemini.")

    model = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    encoded_model = urllib.parse.quote(model, safe="")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{encoded_model}:generateContent"
    # chave no cabeçalho, não na URL: URLs acabam em logs e mensagens de erro
    data = _post_json(url, {"contents": [{"parts": [{"text": prompt}]}]}, {"x-goog-api-key": api_key})

    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("A resposta do Gemini não contém texto gerado.") from exc
    if not isinstance(parts, list):
        raise RuntimeError("A resposta do Gemini não contém texto gerado.")
    text = "".join(
        part["text"]
        for part in parts
        # modelos com raciocínio (Gemma 4) devolvem o raciocínio interno em partes com "thought": true; só a resposta interessa
        if isinstance(part, dict) and isinstance(part.get("text"), str) and not part.get("thought")
    )
    if not text:
        raise RuntimeError("A resposta do Gemini não contém texto gerado.")
    return text


def _generate_ollama(prompt):
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    data = _post_json(
        os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/") + "/api/generate",
        {"model": model, "prompt": prompt, "stream": False},
    )
    text = data.get("response") if isinstance(data, dict) else None
    if not isinstance(text, str) or not text:
        raise RuntimeError("A resposta do Ollama não contém texto gerado.")
    return text


def generate(prompt):
    """Envia um prompt ao backend configurado e retorna o texto gerado."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("O prompt não pode ser vazio.")
    _load_env()

    backend = os.environ.get("LLM_BACKEND", "gemini").strip().lower()
    if backend == "gemini":
        return _generate_gemini(prompt)
    if backend == "ollama":
        return _generate_ollama(prompt)
    raise ValueError("LLM_BACKEND deve ser 'gemini' ou 'ollama'.")


def main():
    parser = argparse.ArgumentParser(description="Envia um prompt ao modelo.")
    parser.add_argument("prompt", help="Texto a enviar ao modelo.")
    args = parser.parse_args()

    try:
        print(generate(args.prompt))
    except (RuntimeError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
