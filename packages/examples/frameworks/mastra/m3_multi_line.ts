/**
 * Example: Mastra + Hymoex M3 (MoE MultiLine).
 *
 * Multiple teams with an integrator routing across them.
 * Each team has a supervisor function coordinating its agents.
 *
 * Requires: npm install @mastra/core
 */

import { Agent, Mastra } from "@mastra/core";

// --- Hymoex M3: Manager -> Integrators -> Expert Manager -> Teams ---

// Finance team agents
const contractsAgent = new Agent({
  name: "contracts",
  instructions: "You are a contracts expert. Draft and review contracts.",
  model: { provider: "OPEN_AI", name: "gpt-4o-mini" },
});

const paymentsAgent = new Agent({
  name: "payments",
  instructions: "You are a payments expert. Process payroll and invoices.",
  model: { provider: "OPEN_AI", name: "gpt-4o-mini" },
});

// HR team agents
const onboardingAgent = new Agent({
  name: "onboarding",
  instructions: "You are an onboarding specialist. Handle new hire processes.",
  model: { provider: "OPEN_AI", name: "gpt-4o-mini" },
});

const complianceAgent = new Agent({
  name: "compliance",
  instructions: "You are a compliance officer. Ensure regulatory compliance.",
  model: { provider: "OPEN_AI", name: "gpt-4o-mini" },
});

const mastra = new Mastra({
  agents: {
    contracts: contractsAgent,
    payments: paymentsAgent,
    onboarding: onboardingAgent,
    compliance: complianceAgent,
  },
});

// Team supervisor functions
async function financeTeam(query: string): Promise<string> {
  const q = query.toLowerCase();
  const agentName = q.includes("contract") ? "contracts" : "payments";
  const agent = mastra.getAgent(agentName);
  const result = await agent.generate(query);
  return `[Finance/${agentName}] ${result.text}`;
}

async function hrTeam(query: string): Promise<string> {
  const q = query.toLowerCase();
  const agentName = q.includes("onboard") ? "onboarding" : "compliance";
  const agent = mastra.getAgent(agentName);
  const result = await agent.generate(query);
  return `[HR/${agentName}] ${result.text}`;
}

// Integrator routes to the right team
async function integrator(query: string): Promise<string> {
  const q = query.toLowerCase();
  if (
    ["contract", "payment", "payroll", "invoice"].some((w) => q.includes(w))
  ) {
    return financeTeam(query);
  }
  return hrTeam(query);
}

async function main() {
  console.log("Mastra + Hymoex M3: Multi-team with integrator routing");
  console.log("Each team function maps to a Hymoex Team Supervisor");
  // const result = await integrator("Set up payroll for the new hire");
  // console.log(result);
}

main();
