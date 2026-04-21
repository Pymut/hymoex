# One-Line MoE Patterns

**Purpose:** Implementation patterns for One-Line Mixture of Experts architecture.

---

## Pattern Overview

**Structure:**
```
Manager → [Expert 1, Expert 2, Expert 3, ...]
```

**Key Characteristics:**
- Flat hierarchy
- Manager directly coordinates experts
- Single expert selected per task
- Simple, straightforward

---

## Pattern 1: Rule-Based Selection

**Concept:** Use explicit rules to select expert.

**Pseudocode:**
```
Manager {
  experts: map<domain, Expert>

  select_expert(message):
    if message.intent == "research":
      return experts["research"]
    elif message.intent == "writing":
      return experts["writing"]
    elif message.intent == "analysis":
      return experts["analysis"]
    else:
      return experts["general"]

  process(message):
    expert = select_expert(message)
    return expert.process(message)
}
```

**Best For:**
- Clear domain boundaries
- Deterministic routing
- Predictable behavior

**Pros:**
- Simple to implement
- Fast execution
- Easy to debug

**Cons:**
- Rigid (doesn't adapt)
- Must update rules for new experts
- Can't handle ambiguous cases

---

## Pattern 2: Capability Matching

**Concept:** Experts declare capabilities, Manager matches message to capabilities.

**Pseudocode:**
```
Expert {
  capabilities: list<string>

  can_handle(message) -> score:
    score = 0
    for capability in self.capabilities:
      if capability in message.content:
        score += 1
    return score
}

Manager {
  experts: list<Expert>

  select_expert(message):
    best_expert = None
    best_score = 0

    for expert in experts:
      score = expert.can_handle(message)
      if score > best_score:
        best_expert = expert
        best_score = score

    return best_expert if best_expert else default_expert

  process(message):
    expert = select_expert(message)
    return expert.process(message)
}
```

**Best For:**
- Dynamic routing
- Overlapping domains
- Easy to add experts

**Pros:**
- Self-documenting (experts declare capabilities)
- Easy to extend (add expert with capabilities)
- Flexible matching

**Cons:**
- More complex selection logic
- Potential for ties (need tie-breaking)
- Performance overhead from scoring

---

## Pattern 3: LLM-Based Selection

**Concept:** Use LLM to decide which expert should handle message.

**Pseudocode:**
```
Manager {
  experts: list<Expert>
  llm: LanguageModel

  select_expert(message):
    expert_descriptions = []
    for expert in experts:
      expert_descriptions.append({
        "name": expert.name,
        "description": expert.description,
        "capabilities": expert.capabilities
      })

    prompt = f"""
    User message: {message.content}

    Available experts:
    {format_experts(expert_descriptions)}

    Which expert should handle this? Return expert name only.
    """

    expert_name = llm.generate(prompt)
    return get_expert_by_name(expert_name)

  process(message):
    expert = select_expert(message)
    return expert.process(message)
}
```

**Best For:**
- Ambiguous domains
- Natural language routing
- Sophisticated matching

**Pros:**
- Handles ambiguity well
- Natural language understanding
- Adapts to complex cases

**Cons:**
- Slower (LLM call overhead)
- Less predictable
- More expensive

---

## Pattern 4: Priority-Based Selection

**Concept:** Experts have priority levels, select highest priority that can handle.

**Pseudocode:**
```
Expert {
  priority: integer  # Higher = more preferred
  domain: string

  can_handle(message) -> boolean:
    return message.domain == self.domain
}

Manager {
  experts: list<Expert>  # Sorted by priority (descending)

  select_expert(message):
    for expert in experts:
      if expert.can_handle(message):
        return expert
    return default_expert

  process(message):
    expert = select_expert(message)
    return expert.process(message)
}
```

**Best For:**
- Specialist vs. generalist experts
- Fallback chains
- Quality tiers

**Pros:**
- Clear preference order
- Natural fallback mechanism
- Simple tie-breaking

**Cons:**
- Must define priorities carefully
- Can ignore lower-priority experts
- Priority maintenance overhead

---

## Pattern 5: Load-Balanced Selection

**Concept:** Distribute work across multiple instances of same expert type.

**Pseudocode:**
```
Manager {
  expert_pools: map<domain, list<Expert>>
  round_robin_index: map<domain, integer>

  select_expert(message):
    domain = determine_domain(message)
    pool = expert_pools[domain]

    # Round-robin selection
    index = round_robin_index[domain]
    expert = pool[index]

    # Update index for next call
    round_robin_index[domain] = (index + 1) % len(pool)

    return expert

  process(message):
    expert = select_expert(message)
    return expert.process(message)
}
```

**Best For:**
- High throughput
- Multiple expert instances
- Load distribution

**Pros:**
- Balances load across instances
- Better resource utilization
- Handles high traffic

**Cons:**
- More complex state management
- Need multiple instances
- Doesn't consider expert load

---

## Pattern 6: Weighted Random Selection

**Concept:** Experts have weights, selection is weighted random.

**Pseudocode:**
```
Expert {
  weight: float  # Probability weight
  domain: string

  can_handle(message) -> boolean:
    return message.domain == self.domain
}

Manager {
  experts: list<Expert>

  select_expert(message):
    # Filter experts that can handle message
    capable_experts = [e for e in experts if e.can_handle(message)]

    # Extract weights
    weights = [e.weight for e in capable_experts]

    # Weighted random selection
    selected = weighted_random_choice(capable_experts, weights)
    return selected

  process(message):
    expert = select_expert(message)
    return expert.process(message)
}
```

**Best For:**
- A/B testing
- Gradual rollouts
- Experimentation

**Pros:**
- Probabilistic behavior
- Good for testing
- Can bias toward preferred experts

**Cons:**
- Non-deterministic
- Harder to debug
- Need statistical analysis

---

## Implementation Styles

### Style 1: Object-Oriented

**Structure:**
```
# Base classes
class Agent:
  def process(self, message): pass
  def can_handle(self, message): pass

class Expert(Agent):
  def __init__(self, domain, tools):
    self.domain = domain
    self.tools = tools

class Manager:
  def __init__(self):
    self.experts = []

  def add_expert(self, expert):
    self.experts.append(expert)

  def process(self, message):
    expert = self.select_expert(message)
    return expert.process(message)
```

**Best For:**
- OOP languages (Python, Java, C#, TypeScript)
- Stateful components
- Inheritance hierarchies

### Style 2: Functional

**Structure:**
```
# Functions and data structures
Agent = { name, process_fn, can_handle_fn }
Expert = { ...Agent, domain, tools }
Manager = { experts }

function create_expert(domain, tools, process_fn):
  return {
    domain: domain,
    tools: tools,
    process: process_fn,
    can_handle: (msg) => msg.domain == domain
  }

function create_manager(experts):
  return {
    experts: experts,
    process: (msg) => {
      expert = select_expert(experts, msg)
      return expert.process(msg)
    }
  }

function select_expert(experts, message):
  # Selection logic
```

**Best For:**
- Functional languages (Elixir, Haskell, Clojure)
- Immutable data
- Composition

### Style 3: Procedural

**Structure:**
```
# Structs and functions
struct Agent {
  name: string
  domain: string
  tools: array<Tool>
}

struct Manager {
  experts: array<Agent>
}

function agent_process(agent, message):
  # Processing logic

function agent_can_handle(agent, message):
  return agent.domain == message.domain

function manager_process(manager, message):
  expert = manager_select_expert(manager, message)
  return agent_process(expert, message)

function manager_select_expert(manager, message):
  # Selection logic
```

**Best For:**
- Procedural languages (C, Go, Rust)
- Performance-critical code
- Simple data structures

---

## Common Variations

### Variation 1: Manager with Fallback

**Concept:** If selected expert fails, try fallback expert.

```
Manager {
  primary_experts: list<Expert>
  fallback_expert: Expert

  process(message):
    try:
      expert = select_expert(message)
      return expert.process(message)
    except ExpertFailure:
      return fallback_expert.process(message)
}
```

### Variation 2: Manager with Broadcasting

**Concept:** Send message to all experts, return first/best response.

```
Manager {
  experts: list<Expert>

  process(message):
    responses = []
    for expert in experts concurrently:
      try:
        response = expert.process(message)
        responses.append(response)
      except:
        continue

    return best_response(responses)
}
```

### Variation 3: Manager with Caching

**Concept:** Cache expert responses for repeated queries.

```
Manager {
  experts: list<Expert>
  cache: Cache

  process(message):
    cache_key = hash(message)

    if cache.has(cache_key):
      return cache.get(cache_key)

    expert = select_expert(message)
    response = expert.process(message)

    cache.set(cache_key, response)
    return response
}
```

### Variation 4: Manager with Preprocessing

**Concept:** Transform message before sending to expert.

```
Manager {
  experts: list<Expert>
  preprocessor: Preprocessor

  process(message):
    processed_message = preprocessor.process(message)
    expert = select_expert(processed_message)
    response = expert.process(processed_message)
    return response
}
```

---

## Testing Patterns

### Test 1: Expert Selection

```
test_expert_selection():
  manager = create_manager()
  manager.add_expert(create_expert("research"))
  manager.add_expert(create_expert("writing"))

  research_msg = create_message(intent="research")
  expert = manager.select_expert(research_msg)

  assert expert.domain == "research"
```

### Test 2: Message Processing

```
test_message_processing():
  expert = create_mock_expert("test", response="test_result")
  manager = create_manager([expert])

  message = create_message(intent="test")
  response = manager.process(message)

  assert response == "test_result"
```

### Test 3: Fallback Behavior

```
test_fallback():
  failing_expert = create_expert_that_fails()
  fallback_expert = create_expert("fallback", response="fallback_result")

  manager = create_manager([failing_expert], fallback=fallback_expert)

  message = create_message(intent="test")
  response = manager.process(message)

  assert response == "fallback_result"
```

---

## Performance Optimization

### Optimization 1: Lazy Expert Initialization

**Problem:** Creating all experts at startup is slow.

**Solution:** Create experts on-demand.

```
Manager {
  expert_factories: map<domain, Factory>
  expert_instances: map<domain, Expert>

  get_expert(domain):
    if not expert_instances.has(domain):
      factory = expert_factories[domain]
      expert_instances[domain] = factory.create()
    return expert_instances[domain]
}
```

### Optimization 2: Parallel Scoring

**Problem:** Scoring experts sequentially is slow.

**Solution:** Score all experts in parallel.

```
Manager {
  select_expert(message):
    scores = parallel_map(
      experts,
      lambda expert: (expert, expert.can_handle(message))
    )

    best_expert, best_score = max(scores, key=lambda x: x[1])
    return best_expert
}
```

### Optimization 3: Early Exit

**Problem:** Checking all experts when first match is sufficient.

**Solution:** Return first expert that can handle (if priority sorted).

```
Manager {
  select_expert(message):
    for expert in experts:  # Sorted by priority
      if expert.can_handle(message):
        return expert  # Early exit
    return default_expert
}
```

---

## Error Handling

### Strategy 1: Fail Fast

```
Manager {
  process(message):
    expert = select_expert(message)
    if not expert:
      raise NoExpertFoundError(message)
    return expert.process(message)
}
```

### Strategy 2: Graceful Degradation

```
Manager {
  process(message):
    expert = select_expert(message)
    if not expert:
      return default_response(message)

    try:
      return expert.process(message)
    except ExpertError:
      return partial_response(message)
}
```

### Strategy 3: Retry with Alternatives

```
Manager {
  process(message):
    candidates = get_all_capable_experts(message)

    for expert in candidates:
      try:
        return expert.process(message)
      except ExpertError:
        continue  # Try next

    raise AllExpertsFailedError(message)
}
```

---

## Anti-Patterns

### Anti-Pattern 1: God Manager

❌ **Bad:**
```
Manager {
  process(message):
    if message.type == "A":
      # Inline domain logic for A
    elif message.type == "B":
      # Inline domain logic for B
    # Manager doing expert's job
}
```

✅ **Good:**
```
Manager {
  process(message):
    expert = select_expert(message)
    return expert.process(message)
    # Manager only coordinates
}
```

### Anti-Pattern 2: Tight Coupling

❌ **Bad:**
```
Manager {
  research_expert: ResearchExpert  # Knows specific type
  writing_expert: WritingExpert

  process(message):
    if message.needs_research:
      return self.research_expert.specific_method()
    # Coupled to specific implementations
}
```

✅ **Good:**
```
Manager {
  experts: list<Agent>  # Generic interface

  process(message):
    expert = select_expert(message)
    return expert.process(message)
    # Depends on interface only
}
```

### Anti-Pattern 3: Selection Logic in Expert

❌ **Bad:**
```
Expert {
  process(message):
    if message.needs_other_expert:
      other_expert = get_other_expert()
      return other_expert.process(message)
    # Expert making routing decisions
}
```

✅ **Good:**
```
Expert {
  process(message):
    return domain_specific_result(message)
    # Expert stays in domain
}

Manager {
  process(message):
    if message.needs_multiple:
      # Manager handles routing
}
```

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
