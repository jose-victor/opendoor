// POST /api/explain — contrato em docs/arquitetura.md.
import { getProject } from "@/lib/projects";
import { LEVELS, WAYS, type ExplainRequest, type ExplainResponse } from "@/lib/types";
import { explain } from "@/lib/gemini";

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

  const explanation = await explain(project, body.profile);
  const status = explanation.ok ? 200 : (explanation.error === "rate_limited" ? 429 : 500);

  return Response.json(explanation satisfies ExplainResponse, { status });
}