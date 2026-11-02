"""Fixed skill vocabulary (the site's filters) and the rules to detect them in each project.

Each skill: id, label, kind (language | framework | tool | area), optional parent and rules.
The site only shows languages and areas: anything with a parent (React, Flask, PyTorch...) counts as its parent
area (see top()), so the filter doesn't turn into a long, fragmented list.
  langs  - GitHub languages (the main one and those with 10% or more of the code)
  deps   - direct dependencies on npm, PyPI or Go (exact name, or a prefix ending in "/", e.g. "@babel/", "k8s.io/")
  topics - the repository's GitHub topics
  words  - words in the description or the name (regex, case-insensitive)
"""
import re

SKILLS = [
    # languages
    {"id": "javascript", "label": "JavaScript", "kind": "language", "langs": ["JavaScript"], "topics": ["javascript", "nodejs", "node"]},
    {"id": "typescript", "label": "TypeScript", "kind": "language", "langs": ["TypeScript"], "deps": ["typescript", "tslib"], "topics": ["typescript"]},
    {"id": "python", "label": "Python", "kind": "language", "langs": ["Python"], "topics": ["python"]},
    {"id": "c", "label": "C", "kind": "language", "langs": ["C"]},
    {"id": "cpp", "label": "C++", "kind": "language", "langs": ["C++"], "topics": ["cpp", "cplusplus"]},
    {"id": "csharp", "label": "C#", "kind": "language", "langs": ["C#"], "topics": ["csharp", "dotnet"]},
    {"id": "go", "label": "Go", "kind": "language", "langs": ["Go"], "topics": ["go", "golang"]},
    {"id": "rust", "label": "Rust", "kind": "language", "langs": ["Rust"], "topics": ["rust"]},
    {"id": "java", "label": "Java", "kind": "language", "langs": ["Java"], "topics": ["java"]},
    {"id": "kotlin", "label": "Kotlin", "kind": "language", "langs": ["Kotlin"], "topics": ["kotlin"]},
    {"id": "ruby", "label": "Ruby", "kind": "language", "langs": ["Ruby"], "topics": ["ruby", "rails"]},
    {"id": "php", "label": "PHP", "kind": "language", "langs": ["PHP"], "topics": ["php"]},
    {"id": "shell", "label": "Shell", "kind": "language", "langs": ["Shell"], "topics": ["bash", "shell"]},
    {"id": "dart", "label": "Dart", "kind": "language", "langs": ["Dart"], "topics": ["dart", "flutter"]},
    {"id": "swift", "label": "Swift", "kind": "language", "langs": ["Swift", "Objective-C"], "topics": ["swift", "ios"]},
    # frameworks and runtimes
    {"id": "nodejs", "label": "Node.js", "kind": "framework", "parent": "javascript", "topics": ["nodejs", "node", "npm"], "words": [r"\bnode(\.js)?\b"]},
    {"id": "react", "label": "React", "kind": "framework", "parent": "frontend", "deps": ["react", "react-dom"], "topics": ["react", "reactjs"], "words": [r"\breact\b"]},
    {"id": "vue", "label": "Vue", "kind": "framework", "parent": "frontend", "deps": ["vue", "@vue/"], "topics": ["vue", "vuejs"], "words": [r"\bvue\b"]},
    {"id": "angular", "label": "Angular", "kind": "framework", "parent": "frontend", "deps": ["@angular/"], "topics": ["angular"], "words": [r"\bangular\b"]},
    {"id": "nextjs", "label": "Next.js", "kind": "framework", "parent": "frontend", "deps": ["next"], "topics": ["nextjs"], "words": [r"\bnext\.js\b"]},
    {"id": "express", "label": "Express", "kind": "framework", "parent": "backend", "deps": ["express"], "topics": ["express", "expressjs"], "words": [r"\bexpress\b"]},
    {"id": "electron", "label": "Electron", "kind": "framework", "parent": "desktop", "deps": ["electron"], "topics": ["electron"], "words": [r"\belectron\b"]},
    {"id": "qt", "label": "Qt", "kind": "framework", "parent": "desktop", "topics": ["qt", "qt5", "qt6", "qml"], "words": [r"\bqt\b"]},
    {"id": "django", "label": "Django", "kind": "framework", "parent": "backend", "topics": ["django"], "words": [r"\bdjango\b"]},
    {"id": "flask", "label": "Flask", "kind": "framework", "parent": "backend", "deps": ["flask"], "topics": ["flask"], "words": [r"\bflask\b"]},
    {"id": "fastapi", "label": "FastAPI", "kind": "framework", "parent": "backend", "deps": ["fastapi"], "topics": ["fastapi"], "words": [r"\bfastapi\b"]},
    {"id": "svelte", "label": "Svelte", "kind": "framework", "parent": "frontend", "deps": ["svelte", "@sveltejs/"], "topics": ["svelte", "sveltekit"], "words": [r"\bsvelte(kit)?\b"]},
    {"id": "tailwind", "label": "Tailwind CSS", "kind": "framework", "parent": "frontend", "deps": ["tailwindcss", "@tailwindcss/"], "topics": ["tailwindcss", "tailwind"], "words": [r"\btailwind(css)?\b"]},
    {"id": "gin", "label": "Gin", "kind": "framework", "parent": "backend", "deps": ["github.com/gin-gonic/gin"], "topics": ["gin", "gin-gonic"], "words": [r"\bgin\b"]},
    {"id": "cobra", "label": "Cobra", "kind": "framework", "parent": "cli", "deps": ["github.com/spf13/cobra"], "topics": ["cobra"], "words": [r"\bcobra\b"]},
    {"id": "pytorch", "label": "PyTorch", "kind": "framework", "parent": "ai", "deps": ["torch"], "topics": ["pytorch", "torch"], "words": [r"\bpytorch\b"]},
    {"id": "huggingface", "label": "Hugging Face", "kind": "framework", "parent": "ai", "deps": ["transformers", "huggingface-hub", "datasets", "@huggingface/"], "topics": ["huggingface", "transformers"], "words": [r"\bhugging ?face\b", r"\btransformers\b"]},
    {"id": "langchain", "label": "LangChain", "kind": "framework", "parent": "ai", "deps": ["langchain", "langchain-core", "@langchain/"], "topics": ["langchain"], "words": [r"\blangchain\b"]},
    {"id": "rails", "label": "Ruby on Rails", "kind": "framework", "parent": "backend", "topics": ["rails", "ruby-on-rails"], "words": [r"\brails\b"]},
    # tools
    {"id": "babel", "label": "Babel", "kind": "tool", "parent": "build", "deps": ["@babel/"], "topics": ["babel"], "words": [r"\bbabel\b"]},
    {"id": "webpack", "label": "Webpack", "kind": "tool", "parent": "build", "deps": ["webpack"], "topics": ["webpack"], "words": [r"\bwebpack\b"]},
    {"id": "vite", "label": "Vite", "kind": "tool", "parent": "build", "deps": ["vite"], "topics": ["vite"], "words": [r"\bvite\b"]},
    {"id": "eslint", "label": "ESLint", "kind": "tool", "parent": "build", "deps": ["eslint"], "topics": ["eslint"], "words": [r"\beslint\b"]},
    {"id": "jest", "label": "Jest", "kind": "tool", "parent": "testing", "deps": ["jest", "@jest/"], "topics": ["jest"], "words": [r"\bjest\b"]},
    {"id": "docker", "label": "Docker", "kind": "tool", "parent": "infra", "topics": ["docker", "containers"], "words": [r"\bdocker\b"]},
    {"id": "sql", "label": "SQL / bancos relacionais", "kind": "tool", "parent": "backend", "deps": ["pg", "mysql", "mysql2", "sqlite3"], "topics": ["postgresql", "mysql", "sqlite", "sql"], "words": [r"\b(postgres|mysql|sqlite|sql)\b"]},
    {"id": "mongodb", "label": "MongoDB", "kind": "tool", "parent": "backend", "deps": ["mongodb", "mongoose"], "topics": ["mongodb"], "words": [r"\bmongo(db)?\b"]},
    {"id": "pandas", "label": "pandas / NumPy", "kind": "tool", "parent": "ai", "deps": ["pandas", "numpy"], "topics": ["pandas", "numpy", "dataframe"], "words": [r"\b(pandas|numpy|dataframes?)\b"]},
    {"id": "kubernetes", "label": "Kubernetes", "kind": "tool", "parent": "infra", "deps": ["k8s.io/", "kubernetes"], "topics": ["kubernetes", "k8s", "helm"], "words": [r"\b(kubernetes|k8s)\b"]},
    {"id": "graphql", "label": "GraphQL", "kind": "tool", "parent": "backend", "deps": ["graphql"], "topics": ["graphql"], "words": [r"\bgraphql\b"]},
    # areas (the project's domain)
    {"id": "frontend", "label": "Frontend web", "kind": "area", "topics": ["frontend", "css", "html", "ui"], "words": [r"\b(dom|css|html|browser|ui|classnames?|jsx|svg)\b"]},
    {"id": "backend", "label": "Backend / servidores", "kind": "area", "topics": ["backend", "server", "api", "http"], "words": [r"\b(http|server|middleware|api|router|request|web framework|log(ger|ging)|cache|caching|lru)\b"]},
    {"id": "cli", "label": "Ferramentas de linha de comando", "kind": "area", "topics": ["cli", "terminal", "command-line"], "words": [r"\b(cli|command[- ]line|terminal|argv|shell)\b"]},
    {"id": "build", "label": "Build, compiladores e tooling JS", "kind": "area", "topics": ["bundler", "build-tool", "compiler"], "words": [r"\b(bundl\w*|build|transpil\w*|compil\w*|minif\w*)\b"]},
    {"id": "testing", "label": "Testes, debug e qualidade", "kind": "area", "topics": ["testing", "test", "coverage"], "words": [r"\b(test\w*|assert\w*|coverage|mock\w*|lint\w*|debug\w*)\b"]},
    {"id": "parsing", "label": "Parsers e formatos de dados", "kind": "area", "topics": ["parser", "json", "yaml"], "words": [r"\b(pars\w+|json|yaml|xml|ast|tokeni\w+|regex\w*|syntax|compress\w*|gzip|brotli|zlib|encod\w*|decod\w*|string\w*)\b"]},
    {"id": "security", "label": "Segurança e criptografia", "kind": "area", "topics": ["security", "cryptography", "crypto", "password-manager"], "words": [r"\b(secur\w*|crypt\w*|hash\w*|password\w*|jwt|tls|ssl|auth\w*)\b"]},
    {"id": "multimedia", "label": "Áudio, vídeo, imagem e jogos", "kind": "area", "topics": ["audio", "video", "image", "streaming", "photography", "music"], "words": [r"\b(audio|video|image\w*|music|stream\w*|photo\w*|media)\b"]},
    {"id": "infra", "label": "Infraestrutura e DevOps", "kind": "area", "topics": ["devops", "infrastructure", "ci", "cloud"], "words": [r"\b(devops|deploy\w*|container\w*|cloud)\b"]},
    {"id": "ai", "label": "IA e ciência de dados", "kind": "area", "deps": ["torch", "tensorflow", "transformers", "scikit-learn", "langchain", "openai", "ollama"], "topics": ["machine-learning", "deep-learning", "ai", "llm", "llama", "artificial-intelligence", "neural-network", "stable-diffusion", "generative-ai"], "words": [r"\b(llms?|machine learning|deep learning|neural|inference|ai|gpt|diffusion|tensors?)\b"]},
    {"id": "data", "label": "Ciência e análise de dados", "kind": "area", "parent": "ai", "deps": ["pandas", "numpy", "scipy", "matplotlib"], "topics": ["data-science", "data-analysis", "data-visualization", "jupyter"], "words": [r"\b(data ?(science|analysis|frames?)|statistic\w*|plot\w*|visuali[sz]ation)\b"]},
    {"id": "games", "label": "Jogos", "kind": "area", "parent": "multimedia", "topics": ["game-engine", "gamedev", "game"], "words": [r"\bgame\w*\b"]},
    {"id": "desktop", "label": "Apps desktop e produtividade", "kind": "area", "topics": ["desktop", "desktop-app", "gui"], "words": [r"\bdesktop\b"]},
    {"id": "productivity", "label": "Produtividade e notas", "kind": "area", "parent": "desktop", "topics": ["note-taking", "notes", "knowledge-base", "productivity", "markdown"], "words": [r"\b(notes?|note-taking|knowledge|markdown|productivity|editor|flashcards?)\b"]},
    {"id": "networking", "label": "Redes e protocolos", "kind": "area", "topics": ["networking", "websocket", "p2p", "bittorrent"], "words": [r"\b(socket\w*|websocket|tcp|udp|dns|proxy|torrent|p2p|ip|ipv[46]|urls?|uri|amqp|mqtt|grpc)\b"]},
    {"id": "streams", "label": "Streams e assincronia", "kind": "area", "parent": "backend", "topics": ["streams", "async", "promise"]},
    {"id": "polyfills", "label": "Polyfills e padrões ECMAScript", "kind": "area", "parent": "build", "topics": ["polyfill", "ecmascript", "shim"], "words": [r"\b(polyfill\w*|shim\w*|ecmascript|es\d{1,4}|spec\w*|intrinsic\w*)\b"]},
]
PARENT = {s["id"]: s.get("parent", s["id"]) for s in SKILLS}
_WORDS = {s["id"]: [re.compile(w, re.IGNORECASE) for w in s.get("words", [])] for s in SKILLS}


def public(skill):
    """What goes into web/public/data/skills.json (contract: id, label, kind)."""
    return {k: skill[k] for k in ("id", "label", "kind")}


def detect(languages, topics, deps, text):
    """A project's skills: {id: source}. deps = direct dependencies (any ecosystem); text = name + description."""
    found = {}
    topics, deps = set(topics), set(deps)
    for s in SKILLS:
        sid = s["id"]
        if set(languages) & set(s.get("langs", [])):
            found.setdefault(sid, "language")
        if topics & set(s.get("topics", [])):
            found.setdefault(sid, "topic")
        for d in s.get("deps", []):
            if (d.endswith("/") and any(x.startswith(d) for x in deps)) or d in deps:
                found.setdefault(sid, "dependency")
        if text and any(w.search(text) for w in _WORDS[sid]):
            found.setdefault(sid, "text")
    return found


def top(found):
    """Ids the site shows (languages and areas), from what detect() found."""
    return sorted({PARENT[i] for i in found})


if __name__ == "__main__":
    assert all(PARENT[p] == p for p in PARENT.values()), "parent must be top-level"
    assert top({"react": "dependency", "flask": "topic", "go": "language"}) == ["backend", "frontend", "go"]
    ids = [s["id"] for s in SKILLS]
    assert len(ids) == len(set(ids)), "duplicate id"
    assert detect(["TypeScript"], [], ["@babel/core", "react"], "A tiny HTTP router") == {
        "typescript": "language", "react": "dependency", "babel": "dependency", "backend": "text"}
    assert detect(["Go"], ["kubernetes"], ["github.com/spf13/cobra", "k8s.io/client-go"], "") == {
        "go": "language", "cobra": "dependency", "kubernetes": "topic"}
    assert {"cpp", "python", "pytorch", "ai"} <= set(detect(["C++", "Python"], [], ["torch"], "LLM inference"))
    assert "polyfills" in detect(["JavaScript"], [], [], "ES spec-compliant shim for Object.hasOwn")
    print(f"{len(SKILLS)} skills, selftest ok")
