# Pydantic AI + Hymoex Mapping ⭐

**Status:** RECOMMENDED STACK

**Why:** Pydantic AI provides fast, type-safe agents. Hymoex provides architectural organization. Perfect combination.

---

## Conceptual Mapping

| Pydantic AI | Hymoex Equivalent |
|-------------|-------------------|
| `Agent` | Expert (specialist agent) |
| `RunContext` | Message context |
| `Tool` | Tool/Executor |
| System prompts | Expert capabilities |
| Result types | Response types |

---

## Approach 1: Pydantic AI Agents AS Hymoex Experts

**Concept:** Use Pydantic AI agents directly as Hymoex Experts.

**Example:**

```python
from pydantic_ai import Agent
from typing import Protocol

# Pydantic AI agent
research_agent = Agent(
    "openai:gpt-4",
    system_prompt="You are a research expert...",
)

writing_agent = Agent(
    "openai:gpt-4",
    system_prompt="You are a writing expert...",
)

# Hymoex Manager coordinates Pydantic AI agents
class Manager:
    def __init__(self):
        self.experts = {
            "research": research_agent,
            "writing": writing_agent,
        }

    def process(self, message: str) -> str:
        # Hymoex routing logic
        expert_name = self.select_expert(message)
        expert = self.experts[expert_name]

        # Execute Pydantic AI agent
        result = expert.run_sync(message)
        return result.data

    def select_expert(self, message: str) -> str:
        # Simple routing logic
        if "research" in message.lower():
            return "research"
        elif "write" in message.lower():
            return "writing"
        return "research"  # default
```

**Benefits:**
- ✅ Type-safe agents (Pydantic)
- ✅ Fast execution
- ✅ Clean routing (Hymoex)
- ✅ Best of both worlds

---

## Approach 2: Hymoex Expert Wrapper

**Concept:** Wrap Pydantic AI agents in Hymoex Expert interface.

**Example:**

```python
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import Any

# Define Hymoex Message protocol
class Message(BaseModel):
    content: str
    intent: str
    metadata: dict[str, Any] = {}

class Response(BaseModel):
    content: str
    expert: str
    metadata: dict[str, Any] = {}

# Hymoex Expert wrapping Pydantic AI agent
class HymoexExpert:
    def __init__(self, name: str, domain: str, system_prompt: str):
        self.name = name
        self.domain = domain
        self.agent = Agent(
            "openai:gpt-4",
            system_prompt=system_prompt,
        )

    def can_handle(self, message: Message) -> bool:
        return message.intent == self.domain

    def process(self, message: Message) -> Response:
        # Execute Pydantic AI agent
        result = self.agent.run_sync(message.content)

        return Response(
            content=result.data,
            expert=self.name,
            metadata={"cost": result.usage().total_tokens if result.usage() else 0},
        )

# Usage
research_expert = HymoexExpert(
    name="ResearchExpert",
    domain="research",
    system_prompt="You are a research expert...",
)

writing_expert = HymoexExpert(
    name="WritingExpert",
    domain="writing",
    system_prompt="You are a writing expert...",
)

class Manager:
    def __init__(self):
        self.experts = [research_expert, writing_expert]

    def process(self, message: Message) -> Response:
        for expert in self.experts:
            if expert.can_handle(message):
                return expert.process(message)

        # Fallback to first expert
        return self.experts[0].process(message)
```

**Benefits:**
- ✅ Clean Hymoex interface
- ✅ Type-safe messages (Pydantic)
- ✅ Consistent API
- ✅ Easy to test

---

## Approach 3: Pydantic AI Tools + Hymoex Architecture

**Concept:** Use Pydantic AI's tool system within Hymoex Experts.

**Example:**

```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool
from dataclasses import dataclass

# Define tools using Pydantic AI
@dataclass
class SearchContext:
    api_key: str

def search_tool(ctx: RunContext[SearchContext], query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Results for: {query}"

# Hymoex Expert using Pydantic AI agent with tools
class ResearchExpert:
    def __init__(self, api_key: str):
        self.name = "ResearchExpert"
        self.domain = "research"

        # Pydantic AI agent with tools
        self.agent = Agent(
            "openai:gpt-4",
            system_prompt="You are a research expert. Use tools to find information.",
            deps_type=SearchContext,
        )
        self.agent.tool(search_tool)

        self.context = SearchContext(api_key=api_key)

    def process(self, message: str) -> str:
        result = self.agent.run_sync(message, deps=self.context)
        return result.data

# Manager coordinates experts
class Manager:
    def __init__(self, api_key: str):
        self.research_expert = ResearchExpert(api_key=api_key)

    def process(self, message: str) -> str:
        return self.research_expert.process(message)
```

**Benefits:**
- ✅ Pydantic AI tool system (type-safe, validated)
- ✅ Hymoex organizational structure
- ✅ Clean separation of concerns

---

## Approach 4: Type-Safe Hymoex with Pydantic Models

**Concept:** Use Pydantic for ALL data structures + Hymoex patterns.

**Example:**

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import Literal
from enum import Enum

# Type-safe messages
class Intent(str, Enum):
    RESEARCH = "research"
    WRITING = "writing"
    ANALYSIS = "analysis"

class Message(BaseModel):
    content: str
    intent: Intent
    priority: int = Field(default=5, ge=0, le=10)

class Response(BaseModel):
    content: str
    expert: str
    confidence: float = Field(ge=0.0, le=1.0)

# Type-safe Expert interface
class Expert(BaseModel):
    name: str
    domain: Intent
    agent: Agent

    class Config:
        arbitrary_types_allowed = True

    def can_handle(self, message: Message) -> bool:
        return message.intent == self.domain

    def process(self, message: Message) -> Response:
        result = self.agent.run_sync(message.content)
        return Response(
            content=result.data,
            expert=self.name,
            confidence=0.95,  # Could extract from agent
        )

# Type-safe Manager
class Manager(BaseModel):
    experts: list[Expert]

    class Config:
        arbitrary_types_allowed = True

    def process(self, message: Message) -> Response:
        expert = self._select_expert(message)
        return expert.process(message)

    def _select_expert(self, message: Message) -> Expert:
        for expert in self.experts:
            if expert.can_handle(message):
                return expert
        return self.experts[0]

# Usage
research_agent = Agent("openai:gpt-4", system_prompt="Research expert")
writing_agent = Agent("openai:gpt-4", system_prompt="Writing expert")

manager = Manager(
    experts=[
        Expert(name="Research", domain=Intent.RESEARCH, agent=research_agent),
        Expert(name="Writing", domain=Intent.WRITING, agent=writing_agent),
    ]
)

# Fully type-safe
message = Message(content="Research AI safety", intent=Intent.RESEARCH)
response = manager.process(message)
```

**Benefits:**
- ✅ Full type safety (Pydantic + type hints)
- ✅ Runtime validation
- ✅ Auto-generated API docs (FastAPI integration)
- ✅ Clean Hymoex architecture

---

## Recommended Patterns

### Pattern 1: One-Line MoE with Pydantic AI

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class Message(BaseModel):
    content: str
    domain: str

class Manager:
    def __init__(self):
        self.experts = {
            "research": Agent("openai:gpt-4", system_prompt="Research expert"),
            "writing": Agent("openai:gpt-4", system_prompt="Writing expert"),
        }

    def process(self, message: Message) -> str:
        agent = self.experts.get(message.domain, self.experts["research"])
        result = agent.run_sync(message.content)
        return result.data
```

### Pattern 2: Supervisor with Pydantic AI

```python
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import Literal

class Message(BaseModel):
    content: str
    strategy: Literal["sequential", "parallel", "moe"]

class Supervisor:
    def __init__(self):
        self.experts = [
            Agent("openai:gpt-4", system_prompt="Expert 1"),
            Agent("openai:gpt-4", system_prompt="Expert 2"),
        ]

    def process(self, message: Message) -> str:
        if message.strategy == "sequential":
            return self._sequential(message.content)
        elif message.strategy == "parallel":
            return self._parallel(message.content)
        else:
            return self._moe(message.content)

    def _sequential(self, content: str) -> str:
        result = content
        for expert in self.experts:
            result = expert.run_sync(result).data
        return result

    def _parallel(self, content: str) -> str:
        results = [expert.run_sync(content).data for expert in self.experts]
        return "\n\n".join(results)

    def _moe(self, content: str) -> str:
        # Select best expert
        expert = self.experts[0]  # Simplified
        return expert.run_sync(content).data

class Manager:
    def __init__(self):
        self.supervisor = Supervisor()

    def process(self, message: Message) -> str:
        return self.supervisor.process(message)
```

---

## Integration with FastAPI

**Benefit:** Pydantic + Hymoex + FastAPI = Type-safe API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_ai import Agent

# Pydantic models (shared by FastAPI and Pydantic AI)
class RequestModel(BaseModel):
    query: str
    domain: str

class ResponseModel(BaseModel):
    result: str
    expert: str

# Hymoex Manager with Pydantic AI
class Manager:
    def __init__(self):
        self.experts = {
            "research": Agent("openai:gpt-4", system_prompt="Research"),
            "writing": Agent("openai:gpt-4", system_prompt="Writing"),
        }

    def process(self, request: RequestModel) -> ResponseModel:
        agent = self.experts.get(request.domain)
        if not agent:
            raise ValueError(f"Unknown domain: {request.domain}")

        result = agent.run_sync(request.query)
        return ResponseModel(result=result.data, expert=request.domain)

# FastAPI app
app = FastAPI()
manager = Manager()

@app.post("/process", response_model=ResponseModel)
async def process_request(request: RequestModel) -> ResponseModel:
    try:
        return manager.process(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Benefits:**
- ✅ Auto-generated API docs
- ✅ Request/response validation
- ✅ Type-safe end-to-end
- ✅ Clean architecture

---

## Async Support

**Pydantic AI supports async, Hymoex patterns work with async:**

```python
from pydantic_ai import Agent
import asyncio

class AsyncManager:
    def __init__(self):
        self.experts = {
            "research": Agent("openai:gpt-4", system_prompt="Research"),
            "writing": Agent("openai:gpt-4", system_prompt="Writing"),
        }

    async def process(self, message: str, domain: str) -> str:
        agent = self.experts[domain]
        result = await agent.run(message)  # Async
        return result.data

    async def process_parallel(self, message: str) -> list[str]:
        # Run all experts in parallel
        tasks = [agent.run(message) for agent in self.experts.values()]
        results = await asyncio.gather(*tasks)
        return [r.data for r in results]

# Usage
manager = AsyncManager()
result = await manager.process("Research AI", "research")
```

---

## Testing with Pydantic AI + Hymoex

```python
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest
import pytest

class Manager:
    def __init__(self):
        self.experts = {
            "research": Agent("openai:gpt-4", system_prompt="Research"),
        }

    def process(self, message: str, domain: str) -> str:
        agent = self.experts[domain]
        result = agent.run_sync(message)
        return result.data

# Test with mocking
@pytest.fixture
def manager():
    return Manager()

def test_manager_routing(manager):
    result = manager.process("Test query", "research")
    assert isinstance(result, str)

def test_manager_with_mock():
    # Create test agent with TestModel
    from pydantic_ai.models.test import TestModel

    test_agent = Agent(TestModel())
    manager = Manager()
    manager.experts["research"] = test_agent

    result = manager.process("Test", "research")
    assert result is not None
```

---

## Performance Optimization

### Optimization 1: Lazy Agent Loading

```python
from pydantic_ai import Agent
from typing import Optional

class LazyExpert:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self._agent: Optional[Agent] = None

    @property
    def agent(self) -> Agent:
        if self._agent is None:
            self._agent = Agent("openai:gpt-4", system_prompt=self.system_prompt)
        return self._agent

    def process(self, message: str) -> str:
        return self.agent.run_sync(message).data

class Manager:
    def __init__(self):
        self.experts = {
            "research": LazyExpert("Research", "Research expert"),
            "writing": LazyExpert("Writing", "Writing expert"),
        }
```

### Optimization 2: Caching

```python
from pydantic_ai import Agent
from functools import lru_cache

class CachedExpert:
    def __init__(self):
        self.agent = Agent("openai:gpt-4", system_prompt="Expert")

    @lru_cache(maxsize=100)
    def process(self, message: str) -> str:
        result = self.agent.run_sync(message)
        return result.data
```

---

## Why Pydantic AI + Hymoex is Recommended

1. **Type Safety**: Pydantic provides runtime validation + type hints
2. **Speed**: Pydantic AI is lightweight, fast
3. **Clean Architecture**: Hymoex provides organizational patterns
4. **Simplicity**: No heavy frameworks, just clean code
5. **Testability**: Easy to mock and test
6. **FastAPI Integration**: Natural fit for APIs
7. **Async Support**: Built-in async/await support
8. **Tool System**: Type-safe tool definitions

---

## Migration from Other Frameworks

### From LangGraph

```python
# Before (LangGraph)
from langgraph.graph import StateGraph

graph = StateGraph()
graph.add_node("research", research_node)
graph.add_node("writing", writing_node)

# After (Pydantic AI + Hymoex)
from pydantic_ai import Agent

class Manager:
    def __init__(self):
        self.research = Agent("openai:gpt-4", system_prompt="Research")
        self.writing = Agent("openai:gpt-4", system_prompt="Writing")

    def process(self, message):
        research_result = self.research.run_sync(message)
        writing_result = self.writing.run_sync(research_result.data)
        return writing_result.data
```

### From CrewAI

```python
# Before (CrewAI)
from crewai import Agent, Crew

agents = [
    Agent(role="Researcher", goal="Research"),
    Agent(role="Writer", goal="Write"),
]
crew = Crew(agents=agents)

# After (Pydantic AI + Hymoex)
from pydantic_ai import Agent

class Manager:
    def __init__(self):
        self.experts = [
            Agent("openai:gpt-4", system_prompt="Researcher"),
            Agent("openai:gpt-4", system_prompt="Writer"),
        ]
```

---

## Summary

**Best For:**
- ✅ New projects
- ✅ Production systems
- ✅ Type-safe requirements
- ✅ FastAPI integration
- ✅ Teams valuing simplicity

**Recommended Architecture:**
- One-Line MoE or Supervisor with Pydantic AI agents
- Type-safe messages with Pydantic models
- Clean Hymoex organizational patterns
- FastAPI for API layer (optional)

**Next Steps:**
1. Install: `pip install pydantic-ai`
2. Start with Approach 1 (simplest)
3. Add type safety with Approach 4
4. Scale with Supervisor pattern as needed

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
