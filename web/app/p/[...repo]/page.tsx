// ProjectView's useParams only exists at runtime: Next 16 requires the Suspense around it.
import { Suspense } from "react";
import ProjectView from "./ProjectView";

export default function ProjectPage() {
  return (
    <Suspense fallback={<main className="p-6">Carregando…</main>}>
      <ProjectView />
    </Suspense>
  );
}
