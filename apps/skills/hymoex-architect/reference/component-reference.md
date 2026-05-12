# Component Reference

**Purpose:** Quick reference for Hymoex components.

---

## Agent

**Type:** Base component

**Interface:**
```
Agent {
  name: string

  process(message: Message) -> Response
  can_handle(message: Message) -> boolean
}
```

**Responsibilities:**
- Process messages
- Determine if can handle message

**When to Use:** Base for all agent types

---

## Expert

**Type:** Specialized Agent

**Interface:**
```
Expert extends Agent {
  domain: string
  tools: list<Tool>

  process(message: Message) -> Response
  use_tool(tool_name: string, params: dict) -> Result
}
```

**Responsibilities:**
- Handle domain-specific tasks
- Use tools to execute
- Return domain results

**When to Use:** Need specialized capabilities

---

## Manager

**Type:** Strategic Coordinator

**Interface:**
```
Manager {
  experts: list<Agent>

  process(message: Message) -> Response
  determine_strategy(message: Message) -> Strategy
  delegate(message: Message, strategy: Strategy) -> list<Response>
  synthesize(responses: list<Response>) -> Response
}
```

**Responsibilities:**
- Determine overall strategy
- Delegate to experts/supervisors
- Synthesize final response

**When to Use:** Top-level orchestration

---

## Supervisor

**Type:** Tactical Coordinator

**Interface:**
```
Supervisor {
  experts: list<Expert>
  routing_strategy: Strategy

  process(message: Message, strategy: Strategy) -> Response
  route(message: Message) -> list<Expert>
  coordinate(experts: list<Expert>, message: Message) -> list<Response>
  aggregate(responses: list<Response>) -> Response
}
```

**Responsibilities:**
- Route to appropriate experts
- Implement coordination strategies
- Aggregate results

**When to Use:** 3+ experts, need coordination

---

## Message

**Type:** Communication Protocol

**Structure:**
```
Message {
  id: string
  sender: string
  recipient: string
  intent: string
  content: any
  metadata: dict
  timestamp: datetime
  priority: integer
}
```

**Purpose:**
- Structured communication
- Routing metadata
- Traceability

---

## Quick Decision Guide

**Choose One-Line MoE if:**
- 1-2 experts
- Independent tasks
- Simple routing

**Choose One-Line Supervisor if:**
- 3-5 experts
- Sequential/parallel workflows
- Need coordination

**Choose MoE MultiLine if:**
- 6+ experts
- Multiple teams
- Distributed systems

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
