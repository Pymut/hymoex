/**
 * Example: Customer Support with Mastra following Hymoex M2 pattern.
 *
 * Demonstrates how to build a One-Line Supervisor (M2) system using
 * Mastra's Agent and Workflow abstractions, following Hymoex patterns.
 *
 * Each Mastra Agent maps to a Hymoex Expert role.
 * The Mastra Workflow acts as the Hymoex Supervisor.
 *
 * Requires: npm install @mastra/core
 */

import { Agent, Mastra } from "@mastra/core";

// --- Hymoex M2 Pattern: Manager -> Supervisor -> Experts ---

// Each agent maps to a Hymoex Expert role
const legalExpert = new Agent({
  name: "legal",
  instructions:
    "You are a legal expert. Handle contracts, compliance, and dispute queries concisely.",
  model: {
    provider: "OPEN_AI",
    name: "gpt-4o-mini",
  },
});

const techExpert = new Agent({
  name: "tech",
  instructions:
    "You are a technical support expert. Diagnose and resolve technical issues concisely.",
  model: {
    provider: "OPEN_AI",
    name: "gpt-4o-mini",
  },
});

const billingExpert = new Agent({
  name: "billing",
  instructions:
    "You are a billing specialist. Handle invoicing and payment queries concisely.",
  model: {
    provider: "OPEN_AI",
    name: "gpt-4o-mini",
  },
});

// Register agents with Mastra
const mastra = new Mastra({
  agents: { legal: legalExpert, tech: techExpert, billing: billingExpert },
});

// --- Supervisor routing (Hymoex Supervisor role) ---

async function supervisorRoute(query: string): Promise<string> {
  const q = query.toLowerCase();
  let expertName: string;

  if (
    ["contract", "legal", "compliance", "dispute"].some((w) => q.includes(w))
  ) {
    expertName = "legal";
  } else if (
    ["error", "api", "bug", "system", "crash"].some((w) => q.includes(w))
  ) {
    expertName = "tech";
  } else {
    expertName = "billing";
  }

  const agent = mastra.getAgent(expertName);
  const response = await agent.generate(query);
  return `[${expertName}] ${response.text}`;
}

// --- Run ---

async function main() {
  console.log(
    "Mastra implementation following Hymoex M2 (One-Line Supervisor) pattern"
  );
  console.log("Each Mastra Agent maps to a Hymoex Expert role");
  console.log("The routing function maps to the Hymoex Supervisor role");
  // Uncomment to run (requires OPENAI_API_KEY):
  // const result = await supervisorRoute("My contract terms were violated");
  // console.log(result);
}

main();
