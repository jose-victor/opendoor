// O useParams do ProjectView só existe em tempo de execução: o Next 16 exige o Suspense em volta.
import { Suspense } from "react";
import ProjectView from "./ProjectView";

export default function ProjectPage() {
  return (
    <Suspense fallback={<main className="p-6">Carregando…</main>}>
      <ProjectView />
    </Suspense>
  );
}
