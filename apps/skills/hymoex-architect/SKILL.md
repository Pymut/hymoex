---
name: hymoex-architect
description: Interactive guide for building multi-agent systems using Hymoex architectural patterns. Use when designing agentic systems, coordinating multiple AI experts, applying clean architecture to agent orchestration, or mapping business problems to multi-agent solutions.
---

# Skill: Hymoex Architect

**Purpose:** Interactive guide to help developers and AI agents understand and apply Hymoex architectural patterns to build agentic systems.

**Key Principle:** Hymoex is a **cognitive architecture blueprint**, not a framework. It provides architectural patterns that can be applied to any technology stack or framework.

---

## What This Skill Does

This skill helps you:
1. **Understand** Hymoex architectural patterns (Manager, Supervisor, Expert, etc.)
2. **Map** your business problem to Hymoex components
3. **Choose** the right modality (One-Line MoE, Supervisor, MultiLine)
4. **Design** system architecture using Clean Code + SOLID principles
5. **Apply** Hymoex patterns to existing frameworks (LangGraph, CrewAI, etc.)
6. **Generate** technical guides, diagrams, and documentation

**What this is NOT:**
- ❌ A code generator for a specific language
- ❌ A rigid framework that you must adopt exactly
- ❌ A replacement for your existing tools

**What this IS:**
- ✅ An architectural thinking tool
- ✅ A pattern library adaptable to any language
- ✅ A guide to structure your agentic systems
- ✅ Compatible with any existing framework

---

## How to Use This Skill

### Basic Usage

```bash
# With a description of what you want to build
/hymoex-architect "I need a customer support system with technical and billing experts"

# Without description - interactive mode
/hymoex-architect
```

### What Happens Next

The skill will:
1. **Analyze** your requirements (or ask questions if needed)
2. **Present options** for architectural approaches
3. **Explain trade-offs** of each option
4. **Generate guides** adapted to your context
5. **Provide diagrams** to visualize the architecture
6. **Suggest next steps** for implementation

---

## Skill Workflow

### Phase 1: Context Analysis (Adaptive)

First, I'll understand your situation:

**Questions I might ask:**
- Do you have existing code or starting from scratch?
- If existing: What framework/stack are you using?
- How many expert domains do you need? (determines modality)
- Will this be distributed across teams? (determines topology)
- Do you need complex coordination? (determines Supervisor pattern)
- Are you migrating from another framework?

**Why these questions matter:**
- **Number of experts** → Suggests modality (MoE, Supervisor, MultiLine)
- **Distributed teams** → Suggests MultiLine pattern
- **Coordination complexity** → Suggests Supervisor pattern
- **Existing framework** → Tailors guidance to work with your tools

### Phase 2: Architectural Options (Flexible, not prescriptive)

Based on your context, I'll present **multiple options** with trade-offs:

**Example:**
```
Based on 3 expert domains, here are your options:

Option A: One-Line MoE Pattern
├─ Pros: Simple, direct, low overhead
├─ Cons: Limited coordination, harder to scale beyond 5 experts
└─ Best for: Straightforward delegation, independent experts

Option B: One-Line Supervisor Pattern
├─ Pros: Better coordination, easier to add experts later
├─ Cons: Slightly more complex, adds routing layer
└─ Best for: Expected growth, need for sequential workflows

Option C: Start simple, evolve later
├─ Pros: Fastest to implement, learn by doing
├─ Cons: May need refactoring if requirements change
└─ Best for: Prototyping, uncertain requirements

Which approach fits your needs? Or would you like a hybrid?
```

### Phase 3: Educational Guidance (Conceptual)

I'll explain the **why** behind recommendations using Hymoex concepts:

**Core Concepts Explained:**
- **Agent Pattern**: Autonomous component with role, capabilities, and communication
- **Manager Pattern**: Strategic coordinator (top-level decision making)
- **Supervisor Pattern**: Tactical coordinator (operational routing)
- **Expert Pattern**: Specialized agent for a specific domain
- **Message Protocol**: Structured communication between components

**Clean Architecture Principles:**
- **Single Responsibility**: Each component has one clear purpose
- **Open/Closed**: Easy to add new experts without changing existing code
- **Dependency Inversion**: High-level components don't depend on low-level details

### Phase 4: Technical Guides (Language-Agnostic)

I'll provide **pseudocode and technical specifications** that you can adapt to your language:

**What you'll get:**
- 📐 Conceptual interfaces (not language-specific code)
- 📊 Architecture diagrams (Mermaid format)
- 📋 Implementation checklists
- 🔄 Flow diagrams showing message passing
- 📚 References to detailed pattern documentation

**What you won't get:**
- ❌ Rigid Python/TypeScript/etc. code you must copy
- ❌ One "correct" implementation
- ❌ Framework-specific prescriptions

### Phase 5: Implementation Support (Adapted to your stack)

I'll help you apply patterns to your specific context:

**If you have existing code:**
- Analyze your current structure
- Suggest how to apply Hymoex patterns incrementally
- Show multiple refactoring paths
- Respect your existing architecture

**If starting fresh:**
- Provide starter templates in pseudocode
- Show multiple implementation approaches
- Guide you through architectural decisions
- Let you choose the style that fits

---

## Decision Guide: Choosing Your Architecture

### Quick Decision Matrix

| Your Situation | Suggested Modality | Reasoning |
|----------------|-------------------|-----------|
| 1-2 expert domains | One-Line MoE | Simplest pattern, direct delegation |
| 3-5 expert domains | One-Line Supervisor | Balance of simplicity and coordination |
| 6+ expert domains | MoE MultiLine | Scalable, supports team distribution |
| Need sequential workflows | Supervisor Pattern | Enables chaining and orchestration |
| Distributed teams | MultiLine Pattern | Supports independent team development |
| Unknown/prototyping | One-Line MoE | Start simple, evolve as needed |

**Note:** These are **suggestions**, not rules. Every system is unique.

---

## Core Patterns Reference

### Pattern 1: Agent (Base Pattern)

**Concept:** Autonomous component with a role, capabilities, and communication interface.

**Conceptual Interface:**
```
Agent {
  properties:
    name: string
    role: string
    capabilities: list<string>

  methods:
    process(message: Message) -> Response
    can_handle(message: Message) -> boolean
}
```

### Pattern 2: Manager (Strategic Coordinator)

**Concept:** Top-level coordinator that determines overall strategy and delegates to specialists.

**Conceptual Interface:**
```
Manager {
  properties:
    name: string
    experts: list<Agent>
    supervisors: list<Supervisor>
    strategy: Strategy

  methods:
    process(message: Message) -> Response
    determine_strategy(message: Message) -> Strategy
    delegate(message: Message, strategy: Strategy) -> list<Response>
    synthesize(responses: list<Response>) -> Response
}
```

### Pattern 3: Supervisor (Tactical Coordinator)

**Concept:** Mid-level coordinator that handles operational routing and orchestration within a domain or team.

**Conceptual Interface:**
```
Supervisor {
  properties:
    name: string
    domain: string
    experts: list<Expert>
    routing_strategy: Strategy

  methods:
    process(message: Message) -> Response
    route(message: Message) -> list<Expert>
    coordinate(experts: list<Expert>, message: Message) -> list<Response>
    aggregate(responses: list<Response>) -> Response
}
```

### Pattern 4: Expert (Specialized Agent)

**Concept:** Domain specialist that executes specific tasks using tools and knowledge.

**Conceptual Interface:**
```
Expert extends Agent {
  properties:
    domain: string
    tools: list<Tool>
    knowledge_base: KnowledgeSource

  methods:
    can_handle(message: Message) -> boolean
    process(message: Message) -> Response
    use_tool(tool_name: string, params: dict) -> Result
}
```

---

## Architectural Modalities

### Modality 1: One-Line MoE (Mixture of Experts)

**When to Use:**
- 1-2 expert domains
- Simple, direct delegation
- Independent tasks (no dependencies)

**Architecture:**
```
┌─────────┐
│ Manager │
└────┬────┘
     │ (selects best expert)
     ├─────┬─────┬─────┐
     ↓     ↓     ↓     ↓
  Expert Expert Expert Expert
```

### Modality 2: One-Line Supervisor

**When to Use:**
- 3-5 expert domains
- Need sequential or conditional workflows
- Want separation between strategy and routing

**Architecture:**
```
┌─────────┐
│ Manager │ (strategic decisions)
└────┬────┘
     ↓
┌────────────┐
│ Supervisor │ (tactical routing)
└──────┬─────┘
       ├─────┬─────┬─────┐
       ↓     ↓     ↓     ↓
    Expert Expert Expert Expert
```

### Modality 3: MoE MultiLine

**When to Use:**
- 6+ expert domains
- Multiple teams developing independently
- Distributed systems

**Architecture:**
```
┌─────────────┐
│  Integrator │ (strategic synthesis)
└──────┬──────┘
       ├────────────────┬────────────────┐
       ↓                ↓                ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ExpertManager1│ │ExpertManager2│ │ExpertManager3│
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
   ┌───┴───┐        ┌───┴───┐        ┌───┴───┐
   ↓       ↓        ↓       ↓        ↓       ↓
Expert  Expert   Expert  Expert   Expert  Expert
```

---

## Framework Integration

### Supported Frameworks

1. **Pydantic AI** ⭐ (Recommended) - See `framework-mappings/pydantic-ai-mapping.md`
2. **LangGraph** - See `framework-mappings/langgraph-mapping.md`
3. **CrewAI** - See `framework-mappings/crewai-mapping.md`
4. **AutoGen** - See `framework-mappings/autogen-mapping.md`
5. **OpenAI Swarm** - See `framework-mappings/openai-swarm-mapping.md`
6. **Mastra** - See `framework-mappings/mastra-mapping.md`

### Integration Philosophy

**Hymoex is not a replacement - it's an architectural lens.**

You can:
- Keep using your existing framework
- Apply Hymoex patterns to organize your code
- Think in Hymoex terms while implementing in framework terms
- Gradually adopt more Hymoex patterns over time

---

## Common Pitfalls and Solutions

### Pitfall 1: Too Many Experts in One-Line MoE
**Problem:** Adding 10+ experts to a Manager leads to complex routing logic.
**Solution:** Migrate to Supervisor pattern or MultiLine.

### Pitfall 2: Experts Doing Manager's Job
**Problem:** Experts making strategic decisions instead of domain-specific work.
**Solution:** Move strategic logic to Manager, keep experts focused on domain.

### Pitfall 3: Tight Coupling Between Experts
**Problem:** Expert A directly calls Expert B, creating dependencies.
**Solution:** All inter-expert communication goes through Manager/Supervisor.

### Pitfall 4: Stateful Experts
**Problem:** Experts maintain state between messages, causing race conditions.
**Solution:** Keep experts stateless; state lives in Manager or external store.

### Pitfall 5: Generic Experts
**Problem:** Creating "GeneralistExpert" that does everything.
**Solution:** Split into specialized experts with clear domains.

---

## Getting Help

During skill execution, you can:
- Ask for clarification: "Explain Manager vs Supervisor"
- Request alternatives: "Show me other approaches"
- Seek trade-offs: "What are pros/cons of MultiLine?"
- Get examples: "Show an example of sequential coordination"

---

## References

- `core-concepts.md` - Fundamental Hymoex concepts
- `decision-guide.md` - Detailed decision-making framework
- `patterns/` - Implementation pattern library
- `examples/` - Example architectures
- `framework-mappings/` - Integration with existing frameworks
- `reference/` - Quick reference documentation

---

## Skill Metadata

**Version:** 1.0.0
**Last Updated:** 2026-02-12
**Compatibility:** All LLMs, all programming languages
**License:** Same as Hymoex project
