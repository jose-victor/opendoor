#!/usr/bin/env python3
"""Minimal client to run prompts through the Gemini API or Ollama."""
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
DEFAULT_OLLAMA_MODEL = ""  # no default: set OLLAMA_MODEL to the model installed in Ollama
REQUEST_TIMEOUT = 60
RETRY_STATUS = {429, 500, 503}  # free-tier limit and instability: retry with growing backoff


def _load_env(path=ROOT / ".env"):
    """Read the root .env (KEY=value format) without overwriting what's already in the environment."""
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
        detail = exc.read().decode("utf-8", "replace")[:300]  # Google's message says whether it was the limit, the model, the key...
        raise RuntimeError(f"The model API responded with HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not connect to the model API: {exc.reason}.") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("The model API returned an invalid JSON response.") from exc


def _generate_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY to use the Gemini backend.")

    model = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    encoded_model = urllib.parse.quote(model, safe="")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{encoded_model}:generateContent"
    # key in the header, not the URL: URLs end up in logs and error messages
    data = _post_json(url, {"contents": [{"parts": [{"text": prompt}]}]}, {"x-goog-api-key": api_key})

    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("The Gemini response contains no generated text.") from exc
    if not isinstance(parts, list):
        raise RuntimeError("The Gemini response contains no generated text.")
    text = "".join(
        part["text"]
        for part in parts
        # reasoning models return their internal reasoning in parts with "thought": true; only the answer matters
        if isinstance(part, dict) and isinstance(part.get("text"), str) and not part.get("thought")
    )
    if not text:
        raise RuntimeError("The Gemini response contains no generated text.")
    return text


def _generate_ollama(prompt):
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    if not model:
        raise RuntimeError("Set OLLAMA_MODEL to use the Ollama backend.")
    data = _post_json(
        os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/") + "/api/generate",
        {"model": model, "prompt": prompt, "stream": False},
    )
    text = data.get("response") if isinstance(data, dict) else None
    if not isinstance(text, str) or not text:
        raise RuntimeError("The Ollama response contains no generated text.")
    return text


def generate(prompt):
    """Send a prompt to the configured backend and return the generated text."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("The prompt cannot be empty.")
    _load_env()

    backend = os.environ.get("LLM_BACKEND", "gemini").strip().lower()
    if backend == "gemini":
        return _generate_gemini(prompt)
    if backend == "ollama":
        return _generate_ollama(prompt)
    raise ValueError("LLM_BACKEND must be 'gemini' or 'ollama'.")


def main():
    parser = argparse.ArgumentParser(description="Send a prompt to the model.")
    parser.add_argument("prompt", help="Text to send to the model.")
    args = parser.parse_args()

    try:
        print(generate(args.prompt))
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
