# Hymoex Architect Skill

**Interactive architectural guidance for building multi-agent systems using Hymoex patterns.**

---

## What is This?

`/hymoex-architect` is a Claude Code skill that helps you:

- Understand Hymoex architectural patterns
- Map business problems to Hymoex components
- Choose the right architecture for your use case
- Apply Hymoex patterns to existing frameworks
- Generate technical specifications and diagrams

---

## Quick Start

### Basic Usage

```bash
# With a description
/hymoex-architect "Build a customer support system with technical and billing experts"

# Interactive mode
/hymoex-architect
```

### What You Get

The skill will:

1. Analyze your requirements
2. Recommend architectural options (with trade-offs)
3. Generate pseudocode and technical specifications
4. Provide architecture diagrams
5. Offer migration guidance if needed

---

## Key Principles

### 1. Hymoex is an Architecture, Not a Framework

You can use Hymoex patterns with:

- Pydantic AI ⭐ (Recommended)
- LangGraph
- CrewAI
- AutoGen
- Vanilla Python/TypeScript/etc.

### 2. Flexible, Not Prescriptive

The skill provides **options and trade-offs**, not rigid rules.

### 3. Language-Agnostic

Guidance uses **pseudocode** adaptable to any language.

### 4. Progressive Complexity

Start simple (One-Line MoE) → Grow as needed (Supervisor → MultiLine)

---

## Architecture Modalities

### One-Line MoE

- **Best for:** 1-2 experts, simple tasks
- **Structure:** Manager → Experts (direct)

### One-Line Supervisor

- **Best for:** 3-5 experts, workflows
- **Structure:** Manager → Supervisor → Experts

### MoE MultiLine

- **Best for:** 6+ experts, distributed teams
- **Structure:** Integrator → Expert Managers → Experts

---

## Skill Contents

```
hymoex-architect/
├── hymoex-architect.md          # Main skill (interactive guide)
├── core-concepts.md             # Fundamental concepts
├── decision-guide.md            # Architecture selection guide
├── patterns/                    # Implementation patterns
│   ├── one-line-moe-patterns.md
│   ├── supervisor-patterns.md
│   └── multiline-patterns.md
├── examples/                    # Example architectures
│   └── simple/
│       └── basic-setup.md
├── framework-mappings/          # Integration guides
│   ├── overview.md
│   ├── pydantic-ai-mapping.md   ⭐ Recommended
│   ├── langgraph-mapping.md
│   ├── crewai-mapping.md
│   ├── autogen-mapping.md
│   ├── openai-swarm-mapping.md
│   └── mastra-mapping.md
└── reference/                   # Quick reference
    └── component-reference.md
```

---

## Example Interactions

### Example 1: Simple System

**You:**

```
/hymoex-architect "Customer support with technical and billing experts"
```

**Skill:**

```
📐 Analyzing Requirements...

Based on your description:
- 2 expert domains
- Likely independent tasks

🎯 Recommended: One-Line MoE

[Provides architecture diagram, pseudocode, and guidance]
```

### Example 2: Complex System

**You:**

```
/hymoex-architect "Research system with 8 experts across 3 teams"
```

**Skill:**

```
📐 Analyzing Requirements...

Based on your description:
- 8 experts, 3 teams
- Distributed structure

🎯 Recommended: MoE MultiLine

Here are multiple approaches:
Option A: Full MultiLine from start (recommended)
Option B: Start with Supervisor, migrate later
Option C: Hybrid approach

[Provides detailed comparison and guidance]
```

### Example 3: Existing Framework

**You:**

```
/hymoex-architect "I have LangGraph code. How do I apply Hymoex?"
```

**Skill:**

```
📐 Analyzing Your Situation...

You have existing LangGraph code.

🎯 Three Paths Forward:

Path 1: Keep LangGraph, Think Hymoex (Recommended)
- Zero code changes
- Apply Hymoex conceptual patterns
- Immediate value

[Provides conceptual mapping and guidance]
```

---

## Framework Integration

### Recommended Stack: Pydantic AI + Hymoex

**Why:**

- Type-safe agents (Pydantic AI)
- Architectural organization (Hymoex)
- Fast, lightweight, production-ready

**See:** `framework-mappings/pydantic-ai-mapping.md`

### Other Frameworks

All mappings follow the same philosophy:
**Hymoex patterns work WITH your framework, not instead of it.**

---

## Key Concepts

### Components

- **Agent**: Base component with process capability
- **Expert**: Specialized agent for a domain
- **Manager**: Strategic coordinator (top-level)
- **Supervisor**: Tactical coordinator (mid-level)
- **Message**: Structured communication protocol

### Patterns

- **MoE (Mixture of Experts)**: Select best expert for task
- **Sequential**: Chain experts (output → input)
- **Parallel**: Run experts concurrently
- **Hierarchical**: Multi-level coordination

---

## Philosophy

### ✅ Do

- Start with simplest architecture that works
- Think in Hymoex terms
- Apply patterns incrementally
- Use with existing frameworks

### ❌ Don't

- Over-engineer initial implementation
- Treat Hymoex as rigid rules
- Abandon working frameworks
- Assume one "correct" way

---

## Getting Help

During skill execution, you can:

- Ask for clarification: "Explain Manager vs Supervisor"
- Request alternatives: "Show me other approaches"
- Seek trade-offs: "What are pros/cons of MultiLine?"
- Get examples: "Show an example of sequential coordination"

---

## Contributing

To extend this skill:

1. **Add new patterns**: Create files in `patterns/`
2. **Add framework mappings**: Create files in `framework-mappings/`
3. **Add examples**: Create files in `examples/`
4. **Update decision logic**: Edit `decision-guide.md`

---

## Version

**Version:** 1.0.0
**Last Updated:** 2026-02-12
**Compatibility:** All LLMs, all programming languages

---

## License

Same as Hymoex project.

---

## Quick Links

- **Main Skill**: `hymoex-architect.md`
- **Core Concepts**: `core-concepts.md`
- **Decision Guide**: `decision-guide.md`
- **Recommended Stack**: `framework-mappings/pydantic-ai-mapping.md`
- **Quick Reference**: `reference/component-reference.md`

**Made with 💚 by the Pymut lab**
