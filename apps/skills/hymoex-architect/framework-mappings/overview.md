# Framework Mappings: Overview

**Purpose:** Understand how Hymoex relates to other agentic frameworks.

---

## Core Philosophy

**Hymoex is NOT a replacement for existing frameworks.**

Hymoex is an **architectural thinking tool** that provides patterns and principles you can apply to ANY framework or codebase.

### What This Means

✅ **You can:**
- Use Hymoex patterns OVER LangGraph
- Think in Hymoex terms while coding in CrewAI
- Organize AutoGen code using Hymoex structure
- Apply Hymoex to vanilla Python/TypeScript
- Mix and match frameworks with Hymoex organization

❌ **You don't need to:**
- Abandon your current framework
- Rewrite working code
- Choose between Hymoex and Framework X
- Learn yet another library

---

## Mapping Approaches

### Approach 1: Conceptual Mapping (Recommended First Step)

**Keep your code as-is, think in Hymoex terms:**

```
Your LangGraph Code:
  StateGraph → Think: "This is my Manager"
  Nodes → Think: "These are my Experts"
  Edges → Think: "This is my Message flow"

You get:
  ✅ Better understanding of your architecture
  ✅ Clearer communication with team
  ✅ Design patterns for future work
  ✅ Zero code changes
```

**Benefits:**
- No refactoring needed
- Immediate value
- No risk
- Team alignment

### Approach 2: Structural Mapping (Incremental Refactoring)

**Reorganize code using Hymoex patterns:**

```
Before:
  # All code mixed together
  def handle_request(req):
    # Routing logic
    # Domain logic
    # Coordination logic

After (Hymoex organization):
  class Manager:
    # Only routing logic

  class Expert:
    # Only domain logic

  class Supervisor:
    # Only coordination logic
```

**Benefits:**
- Better separation of concerns
- Easier to extend
- Still uses your framework
- Gradual migration

### Approach 3: Full Implementation (Complete Adoption)

**Build with Hymoex patterns natively:**

```
# Define Hymoex components directly
manager = Manager(name="MainManager")
supervisor = Supervisor(name="TeamSupervisor")
expert1 = Expert(name="ResearchExpert", domain="research")
expert2 = Expert(name="WritingExpert", domain="writing")

# May or may not use external frameworks for tools
```

**Benefits:**
- Full architectural control
- Clean Hymoex patterns
- Framework-agnostic
- Maximum flexibility

**Trade-offs:**
- More work upfront
- Lose framework features
- More maintenance

---

## Framework Comparison

| Framework | Type | Hymoex Mapping |
|-----------|------|----------------|
| **LangGraph** | Graph-based orchestration | StateGraph = Manager, Nodes = Experts |
| **CrewAI** | Agent teams | Crew = Manager, Agents = Experts |
| **AutoGen** | Multi-agent conversations | GroupChat = Supervisor, Agents = Experts |
| **OpenAI Swarm** | Lightweight routines | Swarm = Manager, Routines = Experts |
| **Mastra** | Workflow framework | Workflows = Manager, Agents = Experts |
| **Pydantic AI** | Type-safe agents | Agents = Experts (recommended base) |

---

## Interoperability Patterns

### Pattern 1: Hymoex Manager + Framework Experts

```
# Manager uses Hymoex pattern
class Manager:
  def __init__(self):
    # Experts are framework-based
    self.langgraph_expert = LangGraphAgent(...)
    self.crewai_expert = CrewAIAgent(...)

  def process(self, message):
    # Hymoex routing logic
    expert = self.select_expert(message)
    return expert.process(message)
```

**Best For:**
- Existing framework code
- Gradual migration
- Multi-framework systems

### Pattern 2: Framework Orchestration + Hymoex Organization

```
# Use LangGraph for execution
from langgraph.graph import StateGraph

# Organize with Hymoex concepts
graph = StateGraph()

# Each node is conceptually a Hymoex Expert
graph.add_node("research_expert", research_node)
graph.add_node("writing_expert", writing_node)

# Graph is conceptually a Hymoex Manager
graph.add_edge("research_expert", "writing_expert")
```

**Best For:**
- Leverage framework features
- Hymoex for organization
- Best of both worlds

### Pattern 3: Hymoex Architecture + Framework Tools

```
# Pure Hymoex components
class ResearchExpert(Expert):
  def __init__(self):
    # Use LangChain for tools
    self.search_tool = LangChainTool(...)

  def process(self, message):
    # Use tool from framework
    results = self.search_tool.run(message.content)
    return results
```

**Best For:**
- Hymoex architecture
- Leverage framework tools
- Clean separation

---

## Migration Strategies

### Strategy 1: Document-First

```
Phase 1: Document existing code in Hymoex terms
  - Identify which components are Managers
  - Identify which components are Experts
  - Map message flows

Phase 2: No code changes yet, just documentation

Phase 3: Team learns Hymoex concepts

Phase 4: Future code follows Hymoex patterns
```

### Strategy 2: Wrapper Pattern

```
Phase 1: Create Hymoex wrappers around existing code
  class HymoexManager:
    def __init__(self, existing_graph):
      self.graph = existing_graph

Phase 2: New features use Hymoex patterns

Phase 3: Gradually migrate old code to wrappers

Phase 4: Remove wrappers, pure Hymoex
```

### Strategy 3: Parallel Implementation

```
Phase 1: Build new features with Hymoex

Phase 2: Old and new code coexist

Phase 3: Migrate critical paths to Hymoex

Phase 4: Deprecate old patterns
```

---

## Recommended Stacks

### Stack 1: Pydantic AI + Hymoex (⭐ Recommended)

**Why:**
- Pydantic AI provides type-safe, lightweight agents
- Hymoex provides architectural organization
- Perfect synergy: fast execution + clear structure

**Use Cases:**
- New projects
- Production systems
- Type-safe requirements

### Stack 2: LangGraph + Hymoex

**Why:**
- LangGraph handles execution and state
- Hymoex provides organizational patterns
- Good for complex workflows

**Use Cases:**
- Existing LangGraph code
- Need graph-based execution
- Complex state management

### Stack 3: Vanilla Language + Hymoex

**Why:**
- Pure Hymoex patterns
- No framework dependencies
- Maximum control

**Use Cases:**
- Simple systems
- Framework-averse teams
- Educational purposes

---

## Framework-Specific Guides

Detailed guides for each framework:

- **LangGraph**: See `langgraph-mapping.md`
- **CrewAI**: See `crewai-mapping.md`
- **AutoGen**: See `autogen-mapping.md`
- **OpenAI Swarm**: See `openai-swarm-mapping.md`
- **Mastra**: See `mastra-mapping.md`
- **Pydantic AI**: See `pydantic-ai-mapping.md` ⭐

---

## Key Takeaways

1. **Hymoex ≠ Framework**: It's architectural patterns
2. **Not Either/Or**: Use Hymoex WITH your framework
3. **Incremental Adoption**: Start with concepts, migrate gradually
4. **Multiple Approaches**: Choose what fits your situation
5. **Recommended Stack**: Pydantic AI + Hymoex for new projects

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
