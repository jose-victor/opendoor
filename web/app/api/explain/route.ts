// POST /api/explain — contrato em docs/arquitetura.md.
// E3: resposta fixa. A2 (Anna) troca o bloco marcado pela chamada a explain() de lib/gemma.ts.
import { getProject } from "@/lib/projects";
import { LEVELS, WAYS, type ExplainRequest, type ExplainResponse } from "@/lib/types";

function fail(status: number, error: Extract<ExplainResponse, { ok: false }>["error"], message: string) {
  return Response.json({ ok: false, error, message } satisfies ExplainResponse, { status });
}

function isRequest(b: unknown): b is ExplainRequest {
  const r = b as ExplainRequest;
  return (
    typeof r?.repo === "string" &&
    Array.isArray(r.profile?.skills) &&
    r.profile.skills.every((s) => typeof s === "string") &&
    LEVELS.includes(r.profile.level) &&
    Array.isArray(r.profile.ways) &&
    r.profile.ways.every((w) => WAYS.includes(w))
  );
}

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  if (!isRequest(body)) return fail(400, "bad_request", "Envie { repo, profile: { skills, level, ways } }.");

  const project = getProject(body.repo);
  if (!project) return fail(404, "not_found", `Projeto ${body.repo} não está no OpenDoor.`);

  // --- início do stub (A2 substitui por: return Response.json(await explain(project, body.profile))) ---
  return Response.json({
    ok: true,
    why: `Resposta de exemplo para ${project.repo}: o Gemma ainda não está ligado (issue A2).`,
    first_steps: ["Leia o README e o CONTRIBUTING.", "Procure issues marcadas para iniciantes.", "Comente na issue antes de começar."],
    heads_up: null,
    model: "stub",
  } satisfies ExplainResponse);
  // --- fim do stub ---
}
