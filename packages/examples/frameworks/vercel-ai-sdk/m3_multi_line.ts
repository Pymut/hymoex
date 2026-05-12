/**
 * Example: Vercel AI SDK + Hymoex M3 (MoE MultiLine).
 *
 * Multiple teams using Vercel AI SDK's multi-step tool execution.
 * Each team exposes its experts as tools. The integrator selects
 * a team tool, which internally delegates to expert tools.
 *
 * Key difference from M2: M2 has flat tools. M3 uses team-level
 * tools that encapsulate their own expert tool sets — nested delegation.
 *
 * Requires: npm install ai @ai-sdk/openai zod
 */

import { generateText, tool } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";

// --- Hymoex M3: Manager -> Integrators -> Expert Manager -> Teams ---

// Finance team experts (internal to the team)
async function financeContracts(request: string): Promise<string> {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system: "You are a contracts expert. Draft or review contracts concisely.",
    prompt: request,
  });
  return result.text;
}

async function financePayments(request: string): Promise<string> {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system: "You are a payments expert. Process payroll and invoices concisely.",
    prompt: request,
  });
  return result.text;
}

// HR team experts (internal to the team)
async function hrOnboarding(request: string): Promise<string> {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system: "You are an onboarding specialist. Handle new hire processes.",
    prompt: request,
  });
  return result.text;
}

async function hrCompliance(request: string): Promise<string> {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system: "You are a compliance officer. Check regulatory requirements.",
    prompt: request,
  });
  return result.text;
}

// Team-level tools — each team encapsulates its own expert selection
// This is the M3 differentiator: tools that contain sub-teams

const financeTeamTool = tool({
  description:
    "Delegate to the finance team for contracts, payments, payroll, and invoicing",
  parameters: z.object({
    request: z.string(),
    subdomain: z.enum(["contracts", "payments"]),
  }),
  execute: async ({ request, subdomain }) => {
    // Team supervisor routes to the right expert within the team
    if (subdomain === "contracts") {
      return financeContracts(request);
    }
    return financePayments(request);
  },
});

const hrTeamTool = tool({
  description:
    "Delegate to the HR team for onboarding, compliance, and new hires",
  parameters: z.object({
    request: z.string(),
    subdomain: z.enum(["onboarding", "compliance"]),
  }),
  execute: async ({ request, subdomain }) => {
    if (subdomain === "onboarding") {
      return hrOnboarding(request);
    }
    return hrCompliance(request);
  },
});

// Integrator — selects which team handles the request
// Uses maxSteps for multi-step tool execution (team selection + expert execution)
async function integratorRoute(query: string) {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system:
      "You are an integrator for enterprise onboarding. Route to the appropriate team and subdomain.",
    prompt: query,
    tools: {
      finance_team: financeTeamTool,
      hr_team: hrTeamTool,
    },
    maxSteps: 3, // Allow multi-step: team selection -> expert execution
  });
  return result;
}

async function main() {
  console.log("Vercel AI SDK + Hymoex M3: Nested tool delegation with maxSteps");
  console.log("Team tools encapsulate expert tools — true M3 composition");
  console.log("M2 = flat tools; M3 = team tools containing sub-experts");
  // const result = await integratorRoute("Draft the employment contract for John");
  // console.log(result);
}

main();
