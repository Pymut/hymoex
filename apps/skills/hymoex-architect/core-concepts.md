# Hymoex Core Concepts

**Purpose:** Fundamental architectural concepts that underpin Hymoex.

This document is a condensed, practical reference - not an academic paper. It contains only the essential concepts a developer needs to understand and apply Hymoex patterns.

---

## What is Hymoex?

**Hymoex** (Hybrid Modular Coordinated Experts) is a **cognitive architecture blueprint** for building multi-agent systems.

### Key Characteristics

1. **Architecture, not Framework**
   - Provides patterns and principles
   - Not tied to specific code or libraries
   - Adaptable to any programming language
   - Works with or without other frameworks

2. **Modular and Composable**
   - Components have clear interfaces
   - Easy to swap implementations
   - Supports incremental adoption

3. **Clean Architecture Foundation**
   - Based on SOLID principles
   - Separation of concerns
   - Dependency inversion
   - Single responsibility

---

## Core Principles

### Principle 1: Separation of Strategic and Tactical Concerns

**Strategic (Manager level):**
- What needs to be done?
- Which domains are involved?
- How should results be synthesized?

**Tactical (Supervisor level):**
- How should experts be coordinated?
- What execution order?
- How to aggregate results?

**Operational (Expert level):**
- Execute specific domain tasks
- Use tools and knowledge
- Return domain results

```
Strategy  →  What to do  →  Manager
Tactics   →  How to do   →  Supervisor
Execution →  Do it       →  Expert
```

### Principle 2: Single Responsibility

**Each component has ONE job:**

- **Manager**: Strategic coordination only
- **Supervisor**: Tactical routing only
- **Expert**: Domain execution only

**Anti-pattern:**
```
❌ Expert making strategic decisions
❌ Manager executing domain logic
❌ Supervisor handling business rules
```

**Good pattern:**
```
✅ Expert focuses on domain expertise
✅ Manager focuses on overall strategy
✅ Supervisor focuses on expert coordination
```

### Principle 3: Message-Based Communication

**All inter-component communication uses structured messages:**

Benefits:
- Type-safe communication
- Traceable execution
- Easier debugging
- Supports async/distributed systems

```
Message {
  id: unique identifier
  sender: source component
  recipient: target component
  intent: what is requested
  content: message payload
  metadata: additional context
}
```

### Principle 4: Loose Coupling

**Components interact through interfaces, not implementations:**

```
Manager knows: "I have experts"
Manager doesn't know: "Expert implementation details"

Expert knows: "I process messages"
Expert doesn't know: "Who sends me messages"
```

Benefits:
- Easy to swap implementations
- Independent testing
- Parallel development
- Framework agnostic

### Principle 5: Progressive Complexity

**Start simple, add complexity only when needed:**

```
Level 1: One-Line MoE (2-3 experts)
  ↓ Growing complexity
Level 2: One-Line Supervisor (3-5 experts)
  ↓ Growing complexity
Level 3: MoE MultiLine (6+ experts, distributed)
```

Don't start with Level 3 if Level 1 suffices.

---

## Fundamental Components

### Component 1: Agent (Base Abstraction)

**Concept:** Autonomous entity that processes messages.

**Properties:**
- Has a name/identifier
- Has capabilities
- Can receive messages
- Can send responses
- Maintains (optional) internal state

**Core Interface:**
```
Agent {
  name: string

  process(message: Message) -> Response
  can_handle(message: Message) -> boolean
}
```

**Autonomy Levels:**

1. **Reactive**: Responds to messages deterministically
2. **Proactive**: Can initiate actions
3. **Goal-directed**: Works toward objectives
4. **Learning**: Adapts behavior over time

**Hymoex focuses on Levels 1-3** (reactive to goal-directed).

### Component 2: Expert (Specialized Agent)

**Concept:** Agent specialized for a specific domain with tools and knowledge.

**Properties:**
- Inherits from Agent
- Has domain focus
- Has specialized tools
- Has domain knowledge
- Returns domain-specific results

**Core Interface:**
```
Expert extends Agent {
  domain: string
  tools: list<Tool>

  can_handle(message: Message) -> boolean
  process(message: Message) -> Response
  use_tool(tool_name: string, params: dict) -> Result
}
```

**Domain Examples:**
- Research Expert → Web search, document analysis
- Writing Expert → Text generation, editing
- Data Expert → Analysis, visualization
- Code Expert → Code generation, debugging

**Key Principle:** One expert = One domain

### Component 3: Manager (Strategic Coordinator)

**Concept:** Top-level component that determines overall strategy.

**Responsibilities:**
- Receive requests from external sources (UI, API)
- Analyze request to determine strategy
- Delegate to appropriate components
- Synthesize final response
- **Does NOT execute domain logic**

**Core Interface:**
```
Manager {
  experts: list<Agent>

  process(message: Message) -> Response
  determine_strategy(message: Message) -> Strategy
  delegate(message: Message, strategy: Strategy) -> list<Response>
  synthesize(responses: list<Response>) -> Response
}
```

**Strategy Types:**
- **Direct**: Single expert handles entire request
- **Parallel**: Multiple experts work concurrently
- **Sequential**: Experts work in chain
- **Hybrid**: Combination of above

**Manager's Mindset:**
```
"I need research AND writing"  → Parallel strategy
"I need research THEN writing" → Sequential strategy
"I need EITHER research OR writing" → MoE strategy
```

### Component 4: Supervisor (Tactical Coordinator)

**Concept:** Mid-level coordinator that handles expert routing within a domain or team.

**Responsibilities:**
- Receive delegated tasks from Manager
- Route to appropriate experts
- Implement coordination strategies
- Aggregate expert results
- Return consolidated response

**Core Interface:**
```
Supervisor {
  experts: list<Expert>
  routing_strategy: Strategy

  process(message: Message) -> Response
  route(message: Message) -> list<Expert>
  coordinate(experts: list<Expert>, message: Message) -> list<Response>
  aggregate(responses: list<Response>) -> Response
}
```

**Coordination Strategies:**

1. **Mixture of Experts (MoE)**:
   ```
   Select single best expert
   Send message to that expert
   Return expert's response
   ```

2. **Sequential**:
   ```
   Send message to Expert 1
   Send Expert 1's output to Expert 2
   Send Expert 2's output to Expert 3
   Return final result
   ```

3. **Parallel**:
   ```
   Send message to all experts concurrently
   Wait for all responses
   Aggregate responses
   Return aggregated result
   ```

**When to Use Supervisor:**
- 3+ experts in a domain
- Need complex routing logic
- Want to separate strategic from tactical concerns
- Expect to add more experts

### Component 5: Message (Communication Protocol)

**Concept:** Structured data format for inter-component communication.

**Properties:**
```
Message {
  # Identity
  id: string (unique identifier)
  timestamp: datetime

  # Routing
  sender: string (component name)
  recipient: string (component name or "broadcast")

  # Intent
  intent: string (task type: "research", "write", "analyze")

  # Payload
  content: any (message data)

  # Context
  metadata: dict (additional information)
  priority: integer (0-10, for queuing)

  # Tracing
  parent_id: string (for message chains)
  trace_id: string (for end-to-end tracing)
}
```

**Message Flow:**
```
1. User creates initial message
2. Manager receives message
3. Manager creates sub-messages for experts
4. Experts process messages
5. Experts return response messages
6. Manager synthesizes into final message
7. User receives final message
```

**Benefits:**
- **Traceable**: Each message has unique ID
- **Structured**: Schema-defined communication
- **Extensible**: Metadata allows additional context
- **Debuggable**: Full message history available

---

## Architectural Patterns

### Pattern 1: Mixture of Experts (MoE)

**Concept:** Select the single best expert for a task.

**How it Works:**
```
1. Analyze incoming message
2. Evaluate each expert's relevance
3. Select best-matching expert
4. Send message to selected expert
5. Return expert's response
```

**Selection Strategies:**

**Strategy A: Rule-Based**
```
if message.intent == "research":
  return ResearchExpert
elif message.intent == "writing":
  return WritingExpert
else:
  return GeneralExpert
```

**Strategy B: Capability Matching**
```
best_expert = None
best_score = 0

for expert in experts:
  score = expert.relevance_score(message)
  if score > best_score:
    best_expert = expert
    best_score = score

return best_expert
```

**Strategy C: LLM-Based**
```
prompt = f"Which expert should handle: {message.content}?"
expert_name = llm.generate(prompt)
return get_expert(expert_name)
```

**When to Use MoE:**
- Tasks are independent
- Only one expert needed per task
- Want to minimize resource usage
- Need fast, efficient routing

**Pros:**
- ✅ Efficient (only one expert activated)
- ✅ Simple to implement
- ✅ Low overhead

**Cons:**
- ❌ Can't leverage multiple experts
- ❌ Selection logic can be complex
- ❌ Single point of failure

### Pattern 2: Sequential Coordination

**Concept:** Chain experts where each expert's output becomes next expert's input.

**How it Works:**
```
1. Send message to Expert 1
2. Expert 1 processes and returns output
3. Transform output into message for Expert 2
4. Expert 2 processes and returns output
5. Continue until chain complete
6. Return final output
```

**Example: Content Creation Pipeline**
```
Message: "Create article about AI"
  ↓
Research Expert: Gather information
  ↓ [research findings]
Outline Expert: Create structure
  ↓ [outline]
Writing Expert: Write content
  ↓ [draft]
Editing Expert: Polish content
  ↓ [final article]
Return final article
```

**When to Use Sequential:**
- Tasks have dependencies
- Output of one expert needed by next
- Need staged processing
- Want quality checkpoints

**Pros:**
- ✅ Supports complex workflows
- ✅ Each stage can validate output
- ✅ Easy to debug (check each stage)

**Cons:**
- ❌ Slower (sequential execution)
- ❌ Failure in one stage blocks rest
- ❌ Harder to parallelize

### Pattern 3: Parallel Coordination

**Concept:** Send same message to multiple experts concurrently, aggregate results.

**How it Works:**
```
1. Send message to all experts concurrently
2. Wait for all responses
3. Aggregate responses
4. Return aggregated result
```

**Example: Comprehensive Research**
```
Message: "Research company X"
  ↓
  ├─→ Web Search Expert → [web results]
  ├─→ News Expert → [news articles]
  ├─→ Financial Expert → [financial data]
  ├─→ Social Media Expert → [social sentiment]
  ↓
Aggregate all results
Return comprehensive report
```

**Aggregation Strategies:**

**Strategy A: Concatenation**
```
return combine_all_responses(responses)
```

**Strategy B: Voting**
```
return most_common_response(responses)
```

**Strategy C: Weighted Synthesis**
```
return weighted_average(responses, expert_weights)
```

**Strategy D: LLM-Based Synthesis**
```
prompt = f"Synthesize these expert responses: {responses}"
return llm.generate(prompt)
```

**When to Use Parallel:**
- Tasks are independent
- Need multiple perspectives
- Want faster execution
- Results can be aggregated

**Pros:**
- ✅ Faster (concurrent execution)
- ✅ Multiple perspectives
- ✅ Fault-tolerant (some failures ok)

**Cons:**
- ❌ Aggregation can be complex
- ❌ Higher resource usage
- ❌ Potential for conflicting results

### Pattern 4: Hierarchical Coordination

**Concept:** Multiple levels of coordinators (Manager → Supervisor → Expert).

**How it Works:**
```
1. Manager receives request
2. Manager determines high-level strategy
3. Manager delegates to Supervisors
4. Supervisors route to their Experts
5. Experts execute and respond
6. Supervisors aggregate team results
7. Manager synthesizes final response
```

**Example: Multi-Team System**
```
Manager
  ↓
  ├─→ Research Supervisor
  │     ├─→ Web Research Expert
  │     ├─→ Academic Research Expert
  │     └─→ Patent Research Expert
  │
  ├─→ Analysis Supervisor
  │     ├─→ Data Analysis Expert
  │     ├─→ Statistical Expert
  │     └─→ Visualization Expert
  │
  └─→ Writing Supervisor
        ├─→ Writing Expert
        └─→ Editing Expert
```

**When to Use Hierarchical:**
- Many experts (6+)
- Clear team/domain boundaries
- Need organizational scalability
- Distributed teams

**Pros:**
- ✅ Scales to many experts
- ✅ Clear organizational structure
- ✅ Team autonomy
- ✅ Parallel team development

**Cons:**
- ❌ More complex architecture
- ❌ Additional coordination layers
- ❌ Potential communication overhead

---

## Architectural Modalities

### Modality 1: One-Line MoE

**Structure:**
```
Manager → [Expert 1, Expert 2, Expert 3, ...]
```

**Characteristics:**
- Flat hierarchy
- Manager directly coordinates experts
- MoE selection at Manager level
- Simple, straightforward

**Best For:**
- 1-3 experts
- Simple use cases
- MVPs and prototypes
- Low coordination complexity

**Scaling Limit:** ~5 experts before routing logic becomes complex

### Modality 2: One-Line Supervisor

**Structure:**
```
Manager → Supervisor → [Expert 1, Expert 2, Expert 3, ...]
```

**Characteristics:**
- Two-level hierarchy
- Manager handles strategy
- Supervisor handles routing
- Support for multiple coordination strategies

**Best For:**
- 3-5 experts
- Need sequential or parallel workflows
- Expected growth
- Clean separation of concerns

**Scaling Limit:** ~8 experts or single team/codebase

### Modality 3: MoE MultiLine

**Structure:**
```
Integrator → [EM 1, EM 2, EM 3, ...]
              ↓     ↓     ↓
          [Experts] [Experts] [Experts]
```

**Characteristics:**
- Three-level hierarchy
- Multiple teams/domains
- Distributed coordination
- Independent development

**Best For:**
- 6+ experts
- Multiple teams
- Distributed systems
- High scalability needs

**Scaling Limit:** No practical limit (scales horizontally)

---

## Clean Architecture Integration

### SOLID Principles in Hymoex

#### Single Responsibility Principle (SRP)

**Each component has one responsibility:**

✅ **Good:**
```
Manager: Strategic coordination
Supervisor: Tactical routing
Expert: Domain execution
```

❌ **Bad:**
```
Manager: Strategy + Routing + Execution
  (violates SRP - too many responsibilities)
```

#### Open/Closed Principle (OCP)

**Open for extension, closed for modification:**

✅ **Good:**
```
# Add new expert without changing Manager
new_expert = CustomExpert()
manager.add_expert(new_expert)
```

❌ **Bad:**
```
# Must modify Manager code to add expert
class Manager:
  def process(self, message):
    if message.needs_custom:
      # Hard-coded logic
```

#### Liskov Substitution Principle (LSP)

**Subtypes must be substitutable:**

✅ **Good:**
```
All Experts implement same interface
Can swap any Expert without breaking system
```

❌ **Bad:**
```
CustomExpert has different interface
Manager needs special handling for it
```

#### Interface Segregation Principle (ISP)

**Clients shouldn't depend on unused interfaces:**

✅ **Good:**
```
Agent interface: process(message)
Expert interface: process(message) + use_tool()
Manager only needs Agent interface
```

❌ **Bad:**
```
Single interface with 20 methods
Most clients only need 2-3 methods
```

#### Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions:**

✅ **Good:**
```
Manager depends on Agent interface
Doesn't care about specific implementations
```

❌ **Bad:**
```
Manager depends on ResearchExpert class
Hard-coded to specific implementation
```

### Layered Architecture

**Hymoex follows clean architecture layers:**

```
┌─────────────────────────────────┐
│     Presentation Layer          │ (UI, API)
├─────────────────────────────────┤
│     Application Layer           │ (Manager, Supervisor)
├─────────────────────────────────┤
│     Domain Layer                │ (Experts, Business Logic)
├─────────────────────────────────┤
│     Infrastructure Layer        │ (Tools, External Services)
└─────────────────────────────────┘
```

**Dependency Direction:**
```
Presentation → Application → Domain → Infrastructure
     (depends on)     (depends on)    (depends on)
```

**Key Point:** Dependencies point inward. Inner layers don't know about outer layers.

---

## Communication Patterns

### Pattern 1: Request-Response

**Synchronous communication:**

```
Client → Manager: Send request
Manager → Expert: Forward request
Expert → Manager: Return response
Manager → Client: Return result
```

**Best For:**
- Interactive applications
- Need immediate response
- Simple workflows

### Pattern 2: Message Queue

**Asynchronous communication:**

```
Client → Queue: Publish message
Manager → Queue: Consume message
Manager → Queue: Publish result
Client → Queue: Consume result
```

**Best For:**
- Distributed systems
- High throughput
- Decoupled components

### Pattern 3: Event-Driven

**Publish-Subscribe:**

```
Expert 1 → Event Bus: Publish "research_complete"
Expert 2 → Event Bus: Subscribe to "research_complete"
Expert 2 → Process event
```

**Best For:**
- Loosely coupled systems
- Multiple subscribers
- Real-time reactions

### Pattern 4: Streaming

**Continuous data flow:**

```
Expert → Stream: Write chunk 1
Expert → Stream: Write chunk 2
Client → Stream: Read chunk 1
Client → Stream: Read chunk 2
```

**Best For:**
- Large responses
- Progressive rendering
- Real-time updates

---

## State Management

### Stateless Experts (Recommended)

**Each message processed independently:**

```
Expert {
  process(message, context):
    # Receives all needed context
    # Doesn't store internal state
    # Returns result
}
```

**Benefits:**
- ✅ Easy to scale horizontally
- ✅ No race conditions
- ✅ Simple testing
- ✅ Easier debugging

### Stateful Components (When Needed)

**State maintained across messages:**

```
Manager {
  conversation_history: list<Message>

  process(message):
    self.conversation_history.append(message)
    # Use history for context
}
```

**When to Use:**
- Conversational systems
- Need context across messages
- Multi-turn interactions

**Challenges:**
- ⚠️ Harder to scale
- ⚠️ Need synchronization
- ⚠️ More complex testing

**Best Practice:** Keep state at highest level (Manager), not in Experts.

---

## Error Handling

### Error Propagation

**Errors should propagate with context:**

```
Expert fails
  ↓ Return error with context
Supervisor handles error
  ↓ Decide: retry, fallback, or propagate
Manager receives error
  ↓ Synthesize user-friendly message
User receives clear error
```

### Error Handling Strategies

#### Strategy 1: Fail Fast
```
if error:
  raise Exception("Expert X failed")
```

**Best for:** Critical errors, development

#### Strategy 2: Graceful Degradation
```
if expert_1_fails:
  try expert_2
if expert_2_fails:
  return partial_result
```

**Best for:** Non-critical errors, production

#### Strategy 3: Retry with Backoff
```
retries = 0
while retries < MAX_RETRIES:
  try:
    return expert.process(message)
  except TransientError:
    retries += 1
    sleep(2 ** retries)  # Exponential backoff
raise Exception("Max retries exceeded")
```

**Best for:** Transient errors, network issues

### Error Types

**Transient Errors:**
- Network timeouts
- Rate limits
- Temporary unavailability
- **Action:** Retry

**Permanent Errors:**
- Invalid input
- Authorization failures
- Resource not found
- **Action:** Propagate to user

**Partial Errors:**
- Some experts succeed, some fail
- **Action:** Return partial results with warnings

---

## Testing Strategies

### Unit Testing

**Test each component in isolation:**

```
test_expert():
  expert = ResearchExpert()
  message = Message(content="test query")
  response = expert.process(message)
  assert response.is_valid()
```

### Integration Testing

**Test component interactions:**

```
test_manager_expert_flow():
  manager = Manager()
  expert = ResearchExpert()
  manager.add_expert(expert)

  message = Message(content="research X")
  response = manager.process(message)

  assert response.from_expert == expert.name
```

### End-to-End Testing

**Test full system flow:**

```
test_full_system():
  system = setup_full_system()
  user_request = "Complete task X"

  result = system.process(user_request)

  assert result.is_complete()
  assert result.quality > threshold
```

### Contract Testing

**Test interface contracts:**

```
test_expert_interface():
  expert = CustomExpert()

  # Verify interface compliance
  assert hasattr(expert, 'process')
  assert hasattr(expert, 'can_handle')

  # Verify behavior contracts
  message = Message(content="test")
  response = expert.process(message)
  assert isinstance(response, Response)
```

---

## Performance Considerations

### Optimization Strategies

#### 1. Parallel Execution
```
Use parallel coordination where possible
Avoid unnecessary sequential dependencies
```

#### 2. Caching
```
Cache expert results for repeated queries
Implement cache invalidation strategy
```

#### 3. Lazy Loading
```
Don't initialize all experts at startup
Load experts on-demand
```

#### 4. Resource Pooling
```
Reuse expensive resources (LLM connections, etc.)
Implement connection pooling
```

#### 5. Load Balancing
```
Distribute work across multiple expert instances
Use round-robin or weighted distribution
```

### Performance Metrics

**Track these metrics:**

- **Latency**: Time to process request
- **Throughput**: Requests per second
- **Expert Utilization**: % time experts are busy
- **Error Rate**: % of failed requests
- **Resource Usage**: CPU, memory, network

---

## Security Considerations

### Input Validation

**Validate all messages:**

```
def process(message):
  if not message.validate():
    raise ValidationError()
  # Process validated message
```

### Authorization

**Check permissions:**

```
def process(message):
  if not has_permission(message.sender, message.intent):
    raise AuthorizationError()
  # Process authorized message
```

### Sandboxing

**Isolate expert execution:**

```
Run experts in isolated environments
Limit resource access
Implement timeouts
```

### Audit Logging

**Log all operations:**

```
log.info(f"Manager received message {message.id}")
log.info(f"Routed to expert {expert.name}")
log.info(f"Returned response {response.id}")
```

---

## Summary

### Core Concepts Recap

1. **Hymoex is an architecture, not a framework**
2. **Three main patterns: MoE, Supervisor, MultiLine**
3. **Components: Agent, Expert, Manager, Supervisor, Message**
4. **Built on Clean Architecture + SOLID principles**
5. **Progressive complexity: start simple, grow as needed**

### Key Takeaways

✅ **Do:**
- Start with simplest architecture that works
- Keep experts focused on single domain
- Use message-based communication
- Apply SOLID principles
- Test components independently

❌ **Don't:**
- Over-engineer initial implementation
- Mix strategic and tactical concerns
- Create tightly coupled components
- Make experts do manager's job
- Ignore error handling

### Next Steps

1. Read `decision-guide.md` for choosing your architecture
2. Explore `patterns/` for implementation guidance
3. Check `examples/` for concrete applications
4. Review `framework-mappings/` if using existing frameworks

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
