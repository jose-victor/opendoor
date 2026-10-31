// A1 (Anna): cliente da Gemini API (Gemma). Só roda no servidor: usa process.env.GEMINI_API_KEY.
// Contrato da saída: ExplainResponse em lib/types.ts e docs/arquitetura.md.
import { GoogleGenAI } from "@google/genai";
import type { ExplainResponse, Project, UserProfile } from "./types";

export async function explain(project: Project, profile: UserProfile): Promise<ExplainResponse> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return {
      ok: false,
      error: "model_error",
      message: "Chave GEMINI_API_KEY não configurada no servidor.",
    };
  }

  const ai = new GoogleGenAI({ apiKey });
  const modelName = process.env.GEMMA_MODEL || "gemma-2-27b-it";

  const prompt = `
Você é o assistente inteligente do OpenDoor, utilizando o modelo aberto Gemma da Google.
Seu objetivo é orientar um contribuidor sobre por que e como começar a ajudar em um projeto open source.

DADOS DO CONTRIBUIDOR:
- Nível: ${profile.level}
- Formas que quer ajudar: ${profile.ways?.length ? profile.ways.join(", ") : "Qualquer forma"}
- Habilidades: ${profile.skills?.join(", ") || "Não especificadas"}

DADOS DO PROJETO:
- Repositório: ${project.repo}
- Descrição: ${project.description || "Sem descrição"}
- Linguagem principal: ${project.language || "Não informada"}
- Habilidades do projeto: ${project.skills?.join(", ") || "Nenhuma listada"}
- Formas de ajuda que mais precisa: ${project.needs?.join(", ") || "Geral"}
- Perfil: ${project.profile}
- Issues para iniciantes abertas: ${project.newcomer_open}
- Mantenedores ativos (24m): ${project.maintainers_24m}
- Taxa de abertura a contribuições externas (openness): ${project.openness !== null ? project.openness : "Não avaliada"}
- Política de IA: ${project.ai_policy?.classification || "silent"} (Evidência: "${project.ai_policy?.evidence || ""}")

REGRAS OBRIGATÓRIAS:
- Responda estritamente em Português do Brasil.
- Retorne EXCLUSIVAMENTE um objeto JSON válido (sem blocos markdown adicionais em volta, sem texto antes ou depois).
- O formato do JSON precisa ser exatamente:
{
  "why": "2 a 3 frases explicando de forma prática a conexão entre o perfil e o projeto.",
  "first_steps": ["passo 1", "passo 2", "passo 3"],
  "heads_up": "Alerta importante sobre política de IA ou número de mantenedores, ou null se não houver alerta."
}
`;

  try {
    const response = await ai.models.generateContent({
      model: modelName,
      contents: prompt,
      config: {
        temperature: 0.2,
      },
    });

    const rawText = (response.text || "").trim();
    // Remove blocos de marcação ```json ... ``` caso o modelo os inclua
    const cleanJson = rawText.replace(/^```json\s*/i, "").replace(/```$/, "").trim();
    const parsed = JSON.parse(cleanJson);

    return {
      ok: true,
      why: parsed.why || "Projeto recomendado com base no seu perfil técnico.",
      first_steps: Array.isArray(parsed.first_steps) ? parsed.first_steps : [
        "Clone o repositório e explore a estrutura do código.",
        "Leia o guia de contribuição (CONTRIBUTING.md).",
        "Procure issues abertas marcadas para iniciantes."
      ],
      heads_up: parsed.heads_up || null,
      model: modelName,
    };
  } catch (error: any) {
    console.error("ERRO DETALHADO DO MODELO:", error);

    if (error?.status === 429 || error?.message?.includes("RESOURCE_EXHAUSTED")) {
      return {
        ok: false,
        error: "rate_limited",
        message: "Limite de requisições atingido. Tente novamente em instantes.",
      };
    }

    return {
      ok: false,
      error: "model_error",
      message: error?.message || "Erro ao gerar explicação pelo modelo.",
    };
  }
}