#!/usr/bin/env python3
"""Cliente mínimo para executar prompts no Gemma via Gemini ou Ollama."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_GEMMA_MODEL = "gemma-4-26b-a4b-it"
DEFAULT_OLLAMA_MODEL = "gemma4:e4b"
REQUEST_TIMEOUT = 60


def _post_json(url, payload):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"A API do modelo respondeu com HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Não foi possível conectar à API do modelo: {exc.reason}.") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("A API do modelo retornou uma resposta JSON inválida.") from exc


def _generate_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Defina GEMINI_API_KEY para usar o backend Gemini.")

    model = os.environ.get("GEMMA_MODEL", DEFAULT_GEMMA_MODEL)
    encoded_model = urllib.parse.quote(model, safe="")
    query = urllib.parse.urlencode({"key": api_key})
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{encoded_model}:generateContent?{query}"
    )
    data = _post_json(url, {"contents": [{"parts": [{"text": prompt}]}]})

    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("A resposta do Gemini não contém texto gerado.") from exc
    if not isinstance(parts, list):
        raise RuntimeError("A resposta do Gemini não contém texto gerado.")
    text = "".join(
        part["text"]
        for part in parts
        if isinstance(part, dict) and isinstance(part.get("text"), str)
    )
    if not text:
        raise RuntimeError("A resposta do Gemini não contém texto gerado.")
    return text


def _generate_ollama(prompt):
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    data = _post_json(
        "http://localhost:11434/api/generate",
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

    backend = os.environ.get("LLM_BACKEND", "gemini").strip().lower()
    if backend == "gemini":
        return _generate_gemini(prompt)
    if backend == "ollama":
        return _generate_ollama(prompt)
    raise ValueError("LLM_BACKEND deve ser 'gemini' ou 'ollama'.")


def main():
    parser = argparse.ArgumentParser(description="Envia um prompt ao Gemma.")
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
