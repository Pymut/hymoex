# Supervisor Patterns

**Purpose:** Implementation patterns for Supervisor-based coordination.

---

## Core Supervisor Pattern

**Structure:**
```
Manager → Supervisor → [Expert 1, Expert 2, Expert 3, ...]
```

**Supervisor Responsibilities:**
- Tactical routing to experts
- Implementing coordination strategies
- Aggregating expert results
- Managing expert lifecycle

---

## Coordination Strategies

### Strategy 1: Mixture of Experts (MoE)

```
Supervisor {
  experts: list<Expert>

  process(message, strategy="moe"):
    best_expert = select_best_expert(message)
    return best_expert.process(message)

  select_best_expert(message):
    # Similar to Manager patterns in one-line-moe-patterns.md
    # But at Supervisor level for team-specific routing
}
```

### Strategy 2: Sequential Execution

```
Supervisor {
  experts: list<Expert>

  process(message, strategy="sequential"):
    current_message = message
    results = []

    for expert in experts:
      result = expert.process(current_message)
      results.append(result)
      current_message = transform_for_next(result)

    return aggregate_sequential(results)
}
```

### Strategy 3: Parallel Execution

```
Supervisor {
  experts: list<Expert>

  process(message, strategy="parallel"):
    responses = []

    for expert in experts concurrently:
      response = expert.process(message)
      responses.append(response)

    return aggregate_parallel(responses)
}
```

### Strategy 4: Conditional Routing

```
Supervisor {
  experts: map<condition, Expert>
  rules: list<Rule>

  process(message, strategy="conditional"):
    for rule in rules:
      if rule.matches(message):
        expert = experts[rule.target]
        return expert.process(message)

    return default_expert.process(message)
}
```

---

## Aggregation Patterns

### Pattern 1: Concatenation

```
aggregate(responses):
  return join_all(responses)
```

### Pattern 2: Voting

```
aggregate(responses):
  votes = count_votes(responses)
  return most_common(votes)
```

### Pattern 3: Weighted Average

```
aggregate(responses):
  weights = get_expert_weights()
  return weighted_sum(responses, weights)
```

### Pattern 4: LLM Synthesis

```
aggregate(responses):
  prompt = f"Synthesize: {responses}"
  return llm.generate(prompt)
```

---

## Manager-Supervisor Interaction

### Pattern 1: Strategy Delegation

```
Manager {
  supervisor: Supervisor

  process(message):
    strategy = determine_strategy(message)
    return supervisor.process(message, strategy)

  determine_strategy(message):
    # Strategic decision at Manager level
    if message.requires_all_experts:
      return "parallel"
    elif message.has_dependencies:
      return "sequential"
    else:
      return "moe"
}
```

### Pattern 2: Multi-Supervisor

```
Manager {
  supervisors: map<domain, Supervisor>

  process(message):
    domain = determine_domain(message)
    supervisor = supervisors[domain]
    return supervisor.process(message)
}
```

---

## Testing

```
test_supervisor_moe():
  supervisor = create_supervisor([expert1, expert2])
  message = create_message("test")

  response = supervisor.process(message, strategy="moe")
  assert response.expert in [expert1.name, expert2.name]

test_supervisor_sequential():
  supervisor = create_supervisor([expert1, expert2])
  message = create_message("test")

  response = supervisor.process(message, strategy="sequential")
  assert response.stages == 2

test_supervisor_parallel():
  supervisor = create_supervisor([expert1, expert2])
  message = create_message("test")

  response = supervisor.process(message, strategy="parallel")
  assert len(response.results) == 2
```

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
