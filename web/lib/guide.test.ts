// Run with `npm test` (node:test; Node strips the types, no extra dependency).
import assert from "node:assert/strict";
import { test } from "node:test";
import { aiPolicyNote, composeGuide, guideFor } from "./guide.ts";
import type { Guide, Project, UserProfile } from "./types.ts";

const guide: Guide = {
  summary: "S",
  common_steps: ["watch", "talk", "third common step is dropped"],
  steps_by_way: { code: ["c1", "c2", "c3"], tests: ["t1"], documentation: ["d1"], triage: ["g1"] },
  heads_up: null,
};
const profile = (over: Partial<UserProfile> = {}): UserProfile => ({ skills: [], level: "experienced", ways: [], ...over });
const texts = (g: ReturnType<typeof composeGuide>) => g.steps.map((s) => s.text);

test("the ways the person picked come first, at most 2 steps each", () => {
  const g = composeGuide(guide, profile({ ways: ["code"] }));
  assert.deepEqual(g.ways, ["code"]);
  assert.deepEqual(texts(g), ["watch", "talk", "c1", "c2"]);
});

test("picked ways the project doesn't need are ignored", () => {
  assert.deepEqual(composeGuide(guide, profile({ ways: ["translation", "tests"] })).ways, ["tests"]);
});

test("a beginner who picked nothing gets low-risk ways first, at most 2", () => {
  assert.deepEqual(composeGuide(guide, profile({ level: "beginner" })).ways, ["tests", "documentation"]);
});

test("otherwise, the project's own ways, at most 2", () => {
  assert.deepEqual(composeGuide(guide, profile()).ways, ["code", "tests"]);
});

test("it always starts with watching and talking, never with opening a PR", () => {
  for (const level of ["beginner", "intermediate", "experienced"] as const)
    assert.deepEqual(texts(composeGuide(guide, profile({ level }))).slice(0, 2), ["watch", "talk"]);
});

test("guideFor: the saved guide, or steps built from the opportunities", () => {
  const base = { description: "D", opportunities: [], ai_policy: { classification: "silent", evidence: "", source_file: "" } };
  assert.equal(guideFor({ ...base, guide } as unknown as Project), guide);
  const built = guideFor({
    ...base,
    guide: null,
    opportunities: [
      { way: "review", source: "data", note: "20 PRs abertos" },
      { way: "review", source: "project", note: "o guia menciona revisão." },
    ],
  } as unknown as Project);
  assert.equal(built.summary, "D");
  assert.deepEqual(built.steps_by_way.review, ["20 PRs abertos.", "O guia menciona revisão."]);
});

test("aiPolicyNote: only for projects that forbid AI or ask for disclosure, with the quote", () => {
  const p = (classification: string, evidence = "") => ({ ai_policy: { classification, evidence, source_file: "" } }) as unknown as Project;
  assert.equal(aiPolicyNote(p("silent")), null);
  assert.equal(aiPolicyNote(p("accepts")), null);
  assert.match(aiPolicyNote(p("forbids", "must be human written")) ?? "", /não aceita.*“must be human written”/);
  assert.match(aiPolicyNote(p("accepts_with_disclosure")) ?? "", /avise quando usar IA\.$/);
});
