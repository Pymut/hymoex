/**
 * Example: Vercel AI SDK + Hymoex M1 (One-Line MoE).
 *
 * Two expert tools working in parallel with no supervisor.
 * The Manager directly invokes both experts and merges results.
 *
 * Requires: npm install ai @ai-sdk/openai zod
 */

import { generateText, tool } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";

// --- Hymoex M1: Manager -> Experts (no Supervisor) ---

const writerExpert = tool({
  description: "Write content on a given topic",
  parameters: z.object({ topic: z.string() }),
  execute: async ({ topic }) => `[Writer] Draft about: ${topic}`,
});

const editorExpert = tool({
  description: "Review and edit content",
  parameters: z.object({ content: z.string() }),
  execute: async ({ content }) => `[Editor] Reviewed: ${content}`,
});

// Manager directly calls experts (no supervisor routing needed)
async function managerRun(query: string) {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system: "You are a content manager. Use the writer tool first, then the editor tool.",
    prompt: query,
    tools: { writer: writerExpert, editor: editorExpert },
  });
  return result;
}

async function main() {
  console.log("Vercel AI SDK + Hymoex M1: Two experts, no supervisor");
  // const result = await managerRun("Write a blog post about AI agents");
  // console.log(result);
}

main();
