"""LLM provider for benchmarks — wraps Google Gemini API.

Provides real embedding generation, text completion, and token counting
for honest benchmark measurements.

Requires GEMINI_API_KEY environment variable.
"""

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load .env from repo root
_env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(_env_path)


@dataclass
class BenchmarkMetrics:
    """Accumulated metrics from benchmark LLM calls."""

    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_calls: int = 0
    latencies_ms: list[float] = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def avg_latency_ms(self) -> float:
        return sum(self.latencies_ms) / len(self.latencies_ms) if self.latencies_ms else 0.0

    def reset(self) -> None:
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_calls = 0
        self.latencies_ms.clear()


class GeminiBenchmarkProvider:
    """Gemini-backed LLM provider for benchmark measurements.

    Tracks real token usage and latency for each call.
    """

    def __init__(
        self,
        model: str = "gemini-3-flash-preview",
        embedding_model: str = "text-embedding-004",
    ):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY environment variable is required")

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.embedding_model = embedding_model
        self.metrics = BenchmarkMetrics()

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text completion and track token usage."""
        start = time.perf_counter()

        contents = prompt
        config = None
        if system_prompt:
            config = genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
            )
        else:
            config = genai.types.GenerateContentConfig(temperature=0.3)

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        elapsed_ms = (time.perf_counter() - start) * 1000
        self.metrics.latencies_ms.append(elapsed_ms)
        self.metrics.total_calls += 1

        if response.usage_metadata:
            self.metrics.total_input_tokens += response.usage_metadata.prompt_token_count or 0
            self.metrics.total_output_tokens += response.usage_metadata.candidates_token_count or 0

        return response.text or ""

    def embed(self, text: str) -> list[float]:
        """Generate embedding vector using Gemini embedding model."""
        start = time.perf_counter()

        result = self.client.models.embed_content(
            model=self.embedding_model,
            contents=text,
        )

        elapsed_ms = (time.perf_counter() - start) * 1000
        self.metrics.latencies_ms.append(elapsed_ms)
        self.metrics.total_calls += 1

        return result.embeddings[0].values

    def route_query(self, query: str, expert_domains: list[str]) -> dict:
        """Ask LLM to route a query to the best expert domain.

        Returns dict with 'selected_domain', 'confidence', and 'reasoning'.
        """
        domain_list = ", ".join(expert_domains)
        prompt = f"""You are an expert routing system. Given a customer query, select the most appropriate expert domain.

Available domains: {domain_list}

Query: "{query}"

Respond in exactly this format (no markdown, no extra text):
DOMAIN: <selected domain>
CONFIDENCE: <0.0-1.0>
REASONING: <one sentence>"""

        response = self.generate(prompt)

        # Parse response
        selected = expert_domains[0]  # fallback
        confidence = 0.5
        reasoning = ""

        for line in response.strip().split("\n"):
            line = line.strip()
            if line.startswith("DOMAIN:"):
                candidate = line.split(":", 1)[1].strip().lower()
                for d in expert_domains:
                    if d.lower() == candidate:
                        selected = d
                        break
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            elif line.startswith("REASONING:"):
                reasoning = line.split(":", 1)[1].strip()

        return {
            "selected_domain": selected,
            "confidence": confidence,
            "reasoning": reasoning,
        }

    def coordinate_agents(
        self,
        task: str,
        agent_roles: list[str],
        topology: str = "flat",
    ) -> dict:
        """Simulate multi-agent coordination and measure token overhead.

        topology: 'flat' (all-to-all), 'supervisor' (hub-spoke), 'hierarchical' (hymoex)
        """
        self.metrics.reset()

        if topology == "flat":
            return self._coordinate_flat(task, agent_roles)
        elif topology == "supervisor":
            return self._coordinate_supervisor(task, agent_roles)
        elif topology == "hierarchical":
            return self._coordinate_hierarchical(task, agent_roles)
        else:
            raise ValueError(f"Unknown topology: {topology}")

    def _coordinate_flat(self, task: str, agent_roles: list[str]) -> dict:
        """Flat MAS: every agent sees all messages."""
        responses = []
        # Each agent generates a response seeing the full task
        for role in agent_roles:
            resp = self.generate(
                f"Task: {task}",
                system_prompt=f"You are a {role} expert. Provide a brief response (2-3 sentences) to the task from your domain perspective.",
            )
            responses.append(resp)

        # Each agent sees all other responses (all-to-all coordination)
        for i, role in enumerate(agent_roles):
            other_responses = "\n".join(
                f"- {agent_roles[j]}: {responses[j]}"
                for j in range(len(agent_roles))
                if j != i
            )
            self.generate(
                f"Task: {task}\n\nOther agent responses:\n{other_responses}\n\nProvide your updated response considering all perspectives.",
                system_prompt=f"You are a {role} expert. Synthesize and respond briefly (2-3 sentences).",
            )

        return {
            "topology": "flat",
            "agents": len(agent_roles),
            "total_tokens": self.metrics.total_tokens,
            "input_tokens": self.metrics.total_input_tokens,
            "output_tokens": self.metrics.total_output_tokens,
            "total_calls": self.metrics.total_calls,
            "avg_latency_ms": self.metrics.avg_latency_ms,
        }

    def _coordinate_supervisor(self, task: str, agent_roles: list[str]) -> dict:
        """Single supervisor: hub-and-spoke coordination."""
        # Supervisor analyzes task and dispatches
        dispatch = self.generate(
            f"Task: {task}\n\nAvailable experts: {', '.join(agent_roles)}\n\nWhich experts should handle this? List the relevant ones.",
            system_prompt="You are a supervisor coordinator. Briefly dispatch tasks (2-3 sentences).",
        )

        # Each expert responds
        responses = []
        for role in agent_roles:
            resp = self.generate(
                f"Task: {task}\n\nSupervisor instruction: {dispatch}",
                system_prompt=f"You are a {role} expert. Provide a brief response (2-3 sentences).",
            )
            responses.append(f"{role}: {resp}")

        # Supervisor synthesizes
        self.generate(
            f"Task: {task}\n\nExpert responses:\n" + "\n".join(responses) + "\n\nSynthesize a final answer.",
            system_prompt="You are a supervisor coordinator. Synthesize briefly (2-3 sentences).",
        )

        return {
            "topology": "supervisor",
            "agents": len(agent_roles) + 1,
            "total_tokens": self.metrics.total_tokens,
            "input_tokens": self.metrics.total_input_tokens,
            "output_tokens": self.metrics.total_output_tokens,
            "total_calls": self.metrics.total_calls,
            "avg_latency_ms": self.metrics.avg_latency_ms,
        }

    def _coordinate_hierarchical(self, task: str, agent_roles: list[str]) -> dict:
        """Hymoex hierarchical: manager -> supervisor -> top-k experts."""
        # Manager routes via MoE gating (select top-k)
        routing = self.route_query(task, agent_roles)
        selected = routing["selected_domain"]

        # Only selected expert(s) respond (top-k = 1 or 2)
        top_k = min(2, len(agent_roles))
        # Get the selected + next best
        selected_roles = [selected]
        for role in agent_roles:
            if role != selected and len(selected_roles) < top_k:
                selected_roles.append(role)

        responses = []
        for role in selected_roles:
            resp = self.generate(
                f"Task: {task}",
                system_prompt=f"You are a {role} expert. Provide a focused response (2-3 sentences).",
            )
            responses.append(f"{role}: {resp}")

        # Supervisor synthesizes only selected expert outputs
        self.generate(
            f"Task: {task}\n\nSelected expert responses:\n" + "\n".join(responses) + "\n\nSynthesize a final answer.",
            system_prompt="You are a supervisor. Synthesize briefly (2-3 sentences).",
        )

        return {
            "topology": "hierarchical",
            "agents": len(agent_roles),
            "selected_experts": selected_roles,
            "total_tokens": self.metrics.total_tokens,
            "input_tokens": self.metrics.total_input_tokens,
            "output_tokens": self.metrics.total_output_tokens,
            "total_calls": self.metrics.total_calls,
            "avg_latency_ms": self.metrics.avg_latency_ms,
        }
