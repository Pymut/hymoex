/**
 * Example: Mastra + Hymoex M1 (One-Line MoE).
 *
 * Two expert agents working directly with no supervisor.
 * The Manager (application code) routes directly to experts.
 *
 * Requires: npm install @mastra/core
 */

import { Agent, Mastra } from "@mastra/core";

// --- Hymoex M1: Manager -> Experts (no Supervisor) ---

const writerAgent = new Agent({
  name: "writer",
  instructions: "You are a content writer. Write compelling copy.",
  model: { provider: "OPEN_AI", name: "gpt-4o-mini" },
});

const editorAgent = new Agent({
  name: "editor",
  instructions: "You are an editor. Review and polish content.",
  model: { provider: "OPEN_AI", name: "gpt-4o-mini" },
});

const mastra = new Mastra({
  agents: { writer: writerAgent, editor: editorAgent },
});

// Manager routing — direct to experts (no supervisor in M1)
async function managerRoute(query: string): Promise<string> {
  const writer = mastra.getAgent("writer");
  const draft = await writer.generate(query);

  const editor = mastra.getAgent("editor");
  const reviewed = await editor.generate(`Review this: ${draft.text}`);

  return reviewed.text;
}

async function main() {
  console.log("Mastra + Hymoex M1: Two agents, no supervisor");
  // const result = await managerRoute("Write a blog post about AI agents");
  // console.log(result);
}

main();
