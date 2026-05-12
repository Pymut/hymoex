import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen gap-8 p-8 text-center">
      <div className="max-w-2xl">
        <h1 className="text-5xl font-bold tracking-tight mb-4">
          Hymoex
        </h1>
        <p className="text-xl text-fd-muted-foreground mb-2">
          Hybrid Modular Coordinated Experts
        </p>
        <p className="text-fd-muted-foreground mb-8">
          A cognitive architecture for scalable multi-agent expert coordination.
          MoE-native gating, progressive migration, framework-agnostic.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/docs"
            className="inline-flex items-center px-6 py-3 rounded-lg bg-fd-primary text-fd-primary-foreground font-medium hover:opacity-90 transition-opacity"
          >
            Get Started
          </Link>
          <Link
            href="https://github.com/Pymut/hymoex"
            className="inline-flex items-center px-6 py-3 rounded-lg border border-fd-border font-medium hover:bg-fd-accent transition-colors"
          >
            GitHub
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mt-8">
        <div className="p-6 rounded-xl border border-fd-border">
          <h3 className="font-semibold mb-2">3 Modalities</h3>
          <p className="text-sm text-fd-muted-foreground">
            One-Line MoE, Supervisor, and MultiLine — pick the right one for your expert count.
          </p>
        </div>
        <div className="p-6 rounded-xl border border-fd-border">
          <h3 className="font-semibold mb-2">MoE Gating</h3>
          <p className="text-sm text-fd-muted-foreground">
            96.7% expert selection accuracy via LLM-based routing.
          </p>
        </div>
        <div className="p-6 rounded-xl border border-fd-border">
          <h3 className="font-semibold mb-2">7 Frameworks</h3>
          <p className="text-sm text-fd-muted-foreground">
            Pydantic AI, LangGraph, CrewAI, AutoGen, Swarm, Vercel AI SDK, Mastra.
          </p>
        </div>
      </div>
    </main>
  );
}
