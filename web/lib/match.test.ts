// Run with `npm test` (node:test; Node strips the types, no extra dependency).
import assert from "node:assert/strict";
import { test } from "node:test";
import { rankProjects } from "./match.ts";
import type { Project, UserProfile } from "./types.ts";

const project = (repo: string, over: Partial<Project> = {}): Project =>
  ({
    repo,
    profile: "open_door",
    needs: ["code"],
    skills: ["javascript"],
    beginner: { ready: true, checks: [] },
    newcomer_open: 0,
    debuts_12m: null,
    acceptance: null,
    stars: 0,
    ...over,
  }) as Project;

const profile = (over: Partial<UserProfile> = {}): UserProfile => ({ skills: [], level: "experienced", ways: [], ...over });
const repos = (ps: Project[]) => ps.map((p) => p.repo);

test("stable never shows up; guardian only for people who are not beginners", () => {
  const ps = [project("a/stable", { profile: "stable" }), project("a/guardian", { profile: "guardian" }), project("a/open")];
  assert.deepEqual(repos(rankProjects(ps, profile({ level: "beginner" }))), ["a/open"]);
  assert.deepEqual(repos(rankProjects(ps, profile({ level: "experienced" }))).sort(), ["a/guardian", "a/open"]);
});

test("beginners only see projects ready for beginners", () => {
  const ps = [project("a/ready"), project("a/not-ready", { beginner: { ready: false, checks: [] } })];
  assert.deepEqual(repos(rankProjects(ps, profile({ level: "beginner" }))), ["a/ready"]);
  assert.equal(rankProjects(ps, profile({ level: "intermediate" })).length, 2);
});

test("picked ways: the project must need at least one of them", () => {
  const ps = [project("a/code", { needs: ["code"] }), project("a/docs", { needs: ["documentation"] })];
  assert.deepEqual(repos(rankProjects(ps, profile({ ways: ["documentation"] }))), ["a/docs"]);
});

test("picked skills and languages must match, except for non-code ways only", () => {
  const langs = new Set(["python", "javascript"]);
  const ps = [
    project("a/js", { skills: ["javascript", "frontend"], needs: ["code", "translation"] }),
    project("a/py", { skills: ["python"], needs: ["code", "translation"] }),
  ];
  assert.deepEqual(repos(rankProjects(ps, profile({ skills: ["python"] }), langs)), ["a/py"]);
  // frontend is in common, but the person also picked a language the project doesn't use
  assert.deepEqual(repos(rankProjects(ps, profile({ skills: ["frontend", "python"] }), langs)), ["a/py"]);
  // translating needs no skill in common
  assert.equal(rankProjects(ps, profile({ skills: ["python"], ways: ["translation"] }), langs).length, 2);
});

test("score: skills in common, level bonus, newcomer issues for beginners, ways in common", () => {
  const ps = [
    project("a/one-skill", { skills: ["javascript"] }),
    project("a/two-skills", { skills: ["javascript", "frontend"] }),
    project("a/needs-hands", { profile: "needs_hands", skills: ["javascript", "frontend"] }),
  ];
  // experienced: needs_hands (+3) beats open_door (+1) with the same skills
  assert.deepEqual(repos(rankProjects(ps, profile({ skills: ["javascript", "frontend"] }))), [
    "a/needs-hands",
    "a/two-skills",
    "a/one-skill",
  ]);
  const beginner = [project("a/plain"), project("a/gfi", { newcomer_open: 3 })];
  assert.deepEqual(repos(rankProjects(beginner, profile({ level: "beginner" }))), ["a/gfi", "a/plain"]);
});

test("ties: debuts, then acceptance, then stars; unknown values go last", () => {
  const ps = [
    project("a/stars", { stars: 900 }),
    project("a/acceptance", { acceptance: 0.5 }),
    project("a/debuts", { debuts_12m: 4, acceptance: 0.1 }),
    project("a/unknown"),
  ];
  assert.deepEqual(repos(rankProjects(ps, profile())), ["a/debuts", "a/acceptance", "a/stars", "a/unknown"]);
});
