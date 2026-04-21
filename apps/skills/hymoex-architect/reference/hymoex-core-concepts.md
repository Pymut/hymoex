# Hymoex: Core Concepts Summary

**Purpose:** Essential concepts from Hymoex - only what developers need to know.

---

## What is Hymoex?

**Hymoex** (Hybrid Modular Coordinated Experts) is a cognitive architecture blueprint for multi-agent systems.

**Key Point:** Hymoex is NOT a framework or library. It's a set of architectural patterns you can apply to any technology stack.

---

## Fundamental Principles

### 1. Separation of Concerns

**Three levels of decision-making:**

```
Strategic Level (Manager)
├─ What needs to be done?
├─ Which domains are involved?
└─ How to synthesize results?

Tactical Level (Supervisor)
├─ How to coordinate experts?
├─ What execution order?
└─ How to aggregate results?

Operational Level (Expert)
├─ Execute domain tasks
├─ Use tools
└─ Return results
```

### 2. SOLID Principles

**Single Responsibility:**
- Manager: Strategy only
- Supervisor: Coordination only
- Expert: Domain execution only

**Open/Closed:**
- Easy to add new experts
- No changes to existing code

**Dependency Inversion:**
- Components depend on interfaces
- Not concrete implementations

### 3. Message-Based Communication

**All components communicate via structured messages:**
- Type-safe
- Traceable
- Debuggable
- Supports async/distributed

### 4. Progressive Complexity

```
Start Simple → Add Complexity When Needed

Level 1: One-Line MoE (2-3 experts)
Level 2: One-Line Supervisor (3-5 experts)
Level 3: MoE MultiLine (6+ experts, distributed)
```

---

## Core Components

### Agent (Base)

**Concept:** Autonomous component that processes messages.

**Interface:**
```
Agent {
  process(message) -> response
  can_handle(message) -> boolean
}
```

**Key:** Base abstraction for all agent types.

### Expert (Specialized Agent)

**Concept:** Domain specialist with tools.

**Interface:**
```
Expert extends Agent {
  domain: string
  tools: list<Tool>

  process(message) -> response
  use_tool(tool_name, params) -> result
}
```

**Key:** One expert = One domain (Single Responsibility)

### Manager (Strategic)

**Concept:** Top-level coordinator.

**Interface:**
```
Manager {
  experts: list<Agent>

  process(message) -> response
  determine_strategy(message) -> strategy
  delegate(message, strategy) -> responses
  synthesize(responses) -> response
}
```

**Key:** Determines WHAT, not HOW. Delegates execution.

### Supervisor (Tactical)

**Concept:** Mid-level coordinator.

**Interface:**
```
Supervisor {
  experts: list<Expert>

  process(message, strategy) -> response
  route(message) -> experts
  coordinate(experts, message) -> responses
  aggregate(responses) -> response
}
```

**Key:** Determines HOW (coordination strategy). Aggregates results.

### Message (Protocol)

**Concept:** Structured communication.

**Structure:**
```
Message {
  id: string
  sender: string
  recipient: string
  intent: string
  content: any
  metadata: dict
}
```

**Key:** Enables tracing, routing, and debugging.

---

## Architectural Modalities

### One-Line MoE

**Structure:** `Manager → Experts`

**When:**
- 1-2 experts
- Independent tasks
- Simple routing

**Pros:** Simple, fast, low overhead
**Cons:** Limited scalability

### One-Line Supervisor

**Structure:** `Manager → Supervisor → Experts`

**When:**
- 3-5 experts
- Sequential/parallel workflows
- Need coordination

**Pros:** Flexible, scalable, clean separation
**Cons:** Additional layer

### MoE MultiLine

**Structure:** `Integrator → Expert Managers → Experts`

**When:**
- 6+ experts
- Multiple teams
- Distributed systems

**Pros:** Highly scalable, team autonomy
**Cons:** Complex, distributed coordination

---

## Coordination Strategies

### Mixture of Experts (MoE)

**How:** Select single best expert.

**When:** Independent tasks, need efficiency.

```
1. Analyze message
2. Score each expert
3. Select best
4. Send to selected expert
5. Return result
```

### Sequential

**How:** Chain experts (output → input).

**When:** Dependencies between tasks.

```
1. Send to Expert 1
2. Expert 1 output → Expert 2 input
3. Expert 2 output → Expert 3 input
4. Continue chain
5. Return final result
```

### Parallel

**How:** All experts process concurrently.

**When:** Independent tasks, need multiple perspectives.

```
1. Send message to all experts
2. All process concurrently
3. Wait for all responses
4. Aggregate results
5. Return combined result
```

---

## Clean Architecture Mapping

```
┌─────────────────────────────────┐
│   Presentation Layer            │ (UI, API)
│   - FastAPI routes              │
│   - Message creation            │
├─────────────────────────────────┤
│   Application Layer             │ (Manager, Supervisor)
│   - Orchestration logic         │
│   - Coordination strategies     │
├─────────────────────────────────┤
│   Domain Layer                  │ (Experts, Business Logic)
│   - Domain-specific processing  │
│   - Expert implementations      │
├─────────────────────────────────┤
│   Infrastructure Layer          │ (Tools, External Services)
│   - LLM APIs                    │
│   - Databases                   │
│   - External APIs               │
└─────────────────────────────────┘

Dependencies flow inward: Presentation → Application → Domain → Infrastructure
```

---

## Key Patterns

### Pattern: Stateless Experts (Recommended)

```
Expert {
  process(message, context):
    # No internal state
    # All context from parameters
    result = execute_with_tools(message, context)
    return result
}
```

**Why:** Easy to scale, no race conditions, simple testing.

### Pattern: Manager with Strategy

```
Manager {
  determine_strategy(message):
    if message.requires_all:
      return "parallel"
    elif message.has_dependencies:
      return "sequential"
    else:
      return "moe"
}
```

**Why:** Separate strategic decisions from execution.

### Pattern: Supervisor with Multiple Strategies

```
Supervisor {
  strategies = {
    "moe": MoEStrategy,
    "sequential": SequentialStrategy,
    "parallel": ParallelStrategy,
  }

  process(message, strategy_name):
    strategy = strategies[strategy_name]
    return strategy.execute(message, experts)
}
```

**Why:** Pluggable, extensible, testable.

---

## Common Anti-Patterns

### ❌ God Manager

**Problem:** Manager doing domain logic.

```
Manager {
  process(message):
    if message.type == "research":
      # Manager doing research work
      results = search_web(message.content)
}
```

**Solution:** Delegate to Expert.

```
Manager {
  process(message):
    expert = select_expert(message)
    return expert.process(message)  # Expert does the work
}
```

### ❌ Tight Coupling

**Problem:** Manager knows specific implementations.

```
Manager {
  research_expert: ResearchExpert  # Concrete type

  process(message):
    return self.research_expert.specific_method()
}
```

**Solution:** Depend on interface.

```
Manager {
  experts: list<Agent>  # Interface

  process(message):
    expert = select_expert(message)
    return expert.process(message)  # Generic interface
}
```

### ❌ Stateful Experts

**Problem:** Expert maintains state across calls.

```
Expert {
  history: list  # State

  process(message):
    self.history.append(message)  # Mutating state
    return process_with_history()
}
```

**Solution:** Pass context as parameter.

```
Expert {
  process(message, context):
    # Context passed in, not stored
    return process_with_context(message, context)
}
```

---

## Testing Strategy

### Unit Tests

```
test_expert():
  expert = ResearchExpert()
  message = create_message("test")

  response = expert.process(message)

  assert response.is_valid()
```

### Integration Tests

```
test_manager_expert_flow():
  manager = Manager([expert1, expert2])
  message = create_message("test")

  response = manager.process(message)

  assert response.from_expert in [expert1.name, expert2.name]
```

### Contract Tests

```
test_expert_interface():
  expert = CustomExpert()

  assert hasattr(expert, 'process')
  assert hasattr(expert, 'can_handle')

  message = create_message("test")
  response = expert.process(message)
  assert isinstance(response, Response)
```

---

## Performance Optimization

### 1. Lazy Loading

```
Don't initialize all experts at startup.
Create experts on-demand.
```

### 2. Caching

```
Cache expert responses for repeated queries.
Implement TTL-based invalidation.
```

### 3. Parallel Execution

```
Use parallel coordination when tasks are independent.
Avoid unnecessary sequential execution.
```

### 4. Connection Pooling

```
Reuse expensive resources (LLM connections, DB connections).
Don't create new connections per request.
```

---

## Error Handling

### Strategy 1: Fail Fast

```
if error:
  raise Exception("Clear error message")
```

**Best for:** Development, critical errors

### Strategy 2: Graceful Degradation

```
try:
  return expert.process(message)
except Error:
  return fallback_expert.process(message)
```

**Best for:** Production, non-critical errors

### Strategy 3: Partial Results

```
responses = []
for expert in experts:
  try:
    responses.append(expert.process(message))
  except Error:
    continue  # Skip failed expert

return aggregate_partial(responses)
```

**Best for:** Parallel execution, fault tolerance

---

## Summary

### Core Principles
1. Separation of concerns (Strategic/Tactical/Operational)
2. SOLID principles
3. Message-based communication
4. Progressive complexity

### Core Components
- Agent (base)
- Expert (specialist)
- Manager (strategic)
- Supervisor (tactical)
- Message (protocol)

### Modalities
- One-Line MoE (simple)
- One-Line Supervisor (balanced)
- MoE MultiLine (scalable)

### Key Takeaways
✅ Start simple, add complexity when needed
✅ Keep experts focused on single domain
✅ Use message-based communication
✅ Apply Clean Architecture principles
✅ Test components independently

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
