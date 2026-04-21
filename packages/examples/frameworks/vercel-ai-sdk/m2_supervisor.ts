/**
 * Example: Customer Support with Vercel AI SDK following Hymoex M2 pattern.
 *
 * Demonstrates how to build a One-Line Supervisor (M2) system using
 * Vercel AI SDK's streamText and tool calling, following Hymoex patterns.
 *
 * The orchestrator function acts as the Hymoex Supervisor.
 * Each tool/function acts as a Hymoex Expert.
 *
 * Requires: npm install ai @ai-sdk/openai
 */

import { generateText, tool } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";

// --- Hymoex M2 Pattern: Manager -> Supervisor -> Experts ---

// Expert tools — each maps to a Hymoex Expert role
const legalExpert = tool({
  description: "Handle legal queries: contracts, compliance, disputes",
  parameters: z.object({ query: z.string() }),
  execute: async ({ query }) => `[Legal] Reviewing: ${query}`,
});

const techExpert = tool({
  description: "Handle technical issues: debugging, API errors, infrastructure",
  parameters: z.object({ query: z.string() }),
  execute: async ({ query }) => `[Tech] Diagnosing: ${query}`,
});

const billingExpert = tool({
  description: "Handle billing: invoices, refunds, payment issues",
  parameters: z.object({ query: z.string() }),
  execute: async ({ query }) => `[Billing] Processing: ${query}`,
});

// Supervisor — routes to the right expert via tool selection
async function supervisorRoute(customerQuery: string) {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    // The Supervisor's system prompt defines its Hymoex role
    system:
      "You are a customer support supervisor. Route the query to the correct expert by calling the appropriate tool.",
    prompt: customerQuery,
    tools: {
      legal: legalExpert,
      tech: techExpert,
      billing: billingExpert,
    },
  });
  return result;
}

// --- Run ---

async function main() {
  console.log(
    "Vercel AI SDK implementation following Hymoex M2 (One-Line Supervisor) pattern"
  );
  console.log("Each tool maps to a Hymoex Expert role");
  console.log("The orchestrator maps to the Hymoex Supervisor role");
  // Uncomment to run (requires OPENAI_API_KEY):
  // const result = await supervisorRoute("My contract terms were violated");
  // console.log(result);
}

main();
