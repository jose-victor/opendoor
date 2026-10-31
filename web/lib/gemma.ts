// A1 (Anna): cliente da Gemini API (Gemma 4). Só roda no servidor: usa process.env.GEMINI_API_KEY.
// Contrato da saída: ExplainResponse em lib/types.ts e docs/arquitetura.md.
import { GoogleGenAI, Type, Schema } from "@google/genai";
import type { ExplainResponse, Project, UserProfile } from "./types";

const explainSchema: Schema = {
  type: Type.OBJECT,
  properties: {
    why: {
      type: Type.STRING,
      description: "2 a 3 frases em português explicando por que o projeto combina com o perfil da pessoa.",
    },
    first_steps: {
      type: Type.ARRAY,
      items: { type: Type.STRING },
      description: "De 3 a 5 passos concretos para a pessoa começar a contribuir.",
    },
    heads_up: {
      type: Type.STRING,
      description: "Alerta importante sobre o projeto (política de IA, número de mantenedores, etc.) ou null.",
      nullable: true,
    },
  },
  required: ["why", "first_steps"],
};

export async function explain(project: Project, profile: UserProfile): Promise<ExplainResponse> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.error("ERRO: GEMINI_API_KEY não encontrada no process.env!");
    return {
      ok: false,
      error: "model_error",
      message: "Chave GEMINI_API_KEY não configurada no servidor.",
    };
  }

  const ai = new GoogleGenAI({ apiKey });
  // Usa o modelo configurado no .env ou fallback padrão
  const modelName = process.env.GEMMA_MODEL || "gemini-2.5-flash";

  const prompt = `
Você é o assistente inteligente do OpenDoor.
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

REGRAS:
- Responda em Português do Brasil.
- 'why': 2 a 3 frases práticas conectando o perfil ao projeto.
- 'first_steps': 3 a 5 passos diretos para começar.
- 'heads_up': Se houver restrições de IA (${project.ai_policy?.classification}) ou poucos mantenedores (${project.maintainers_24m}), mencione. Senão, passe null.
`;

  try {
    const response = await ai.models.generateContent({
      model: modelName,
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: explainSchema,
        temperature: 0.2,
      },
    });

    const parsed = JSON.parse(response.text || "{}");

    return {
      ok: true,
      why: parsed.why,
      first_steps: parsed.first_steps || [],
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