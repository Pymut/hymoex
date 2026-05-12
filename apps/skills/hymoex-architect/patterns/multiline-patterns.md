# MultiLine Patterns

**Purpose:** Implementation patterns for distributed, multi-team architectures.

---

## Core MultiLine Pattern

**Structure:**
```
Integrator → [Expert Manager 1, Expert Manager 2, Expert Manager 3, ...]
              ↓                ↓                ↓
          [Experts]        [Experts]        [Experts]
```

**Key Characteristics:**
- Three-level hierarchy
- Multiple independent teams
- Distributed coordination
- Async communication

---

## Integrator Pattern

```
Integrator {
  expert_managers: list<ExpertManager>

  process(message):
    strategy = determine_global_strategy(message)
    managers = select_managers(message, strategy)

    responses = coordinate_managers(managers, message)

    return synthesize_global(responses)

  coordinate_managers(managers, message):
    if strategy is "parallel":
      return parallel_coordinate(managers, message)
    elif strategy is "sequential":
      return sequential_coordinate(managers, message)
    else:
      return selective_coordinate(managers, message)
}
```

---

## Expert Manager Pattern

```
ExpertManager {
  domain: string
  supervisor: Supervisor
  experts: list<Expert>

  process(message):
    # Local coordination within team
    local_strategy = determine_local_strategy(message)
    return supervisor.process(message, local_strategy)
}
```

---

## Communication Patterns

### Pattern 1: Message Queue

```
Integrator {
  message_queue: Queue

  process(message):
    # Publish to queue
    for manager in relevant_managers:
      queue.publish(f"{manager.domain}.requests", message)

    # Collect responses
    responses = []
    for manager in relevant_managers:
      response = queue.consume(f"{manager.domain}.responses")
      responses.append(response)

    return synthesize(responses)
}
```

### Pattern 2: HTTP API

```
Integrator {
  manager_endpoints: map<domain, URL>

  process(message):
    responses = []

    for domain in relevant_domains:
      endpoint = manager_endpoints[domain]
      response = http_post(endpoint, message)
      responses.append(response)

    return synthesize(responses)
}
```

### Pattern 3: gRPC

```
Integrator {
  manager_clients: map<domain, gRPCClient>

  process(message):
    responses = []

    for domain in relevant_domains:
      client = manager_clients[domain]
      response = client.ProcessMessage(message)
      responses.append(response)

    return synthesize(responses)
}
```

---

## Team Isolation Pattern

```
Team A Codebase:
  ExpertManager {
    supervisor: Supervisor
    experts: [Expert1, Expert2, Expert3]

    # Autonomous team decisions
    # Independent deployment
    # Own technology choices
  }

Team B Codebase:
  ExpertManager {
    # Different language/framework OK
    # Different coordination strategy OK
    # Only interface must match
  }
```

---

## Failure Handling

### Pattern 1: Timeout

```
Integrator {
  process(message):
    responses = []

    for manager in managers:
      try:
        response = manager.process(message, timeout=5s)
        responses.append(response)
      except TimeoutError:
        # Continue without this manager
        pass

    return synthesize_partial(responses)
}
```

### Pattern 2: Circuit Breaker

```
Integrator {
  circuit_breakers: map<domain, CircuitBreaker>

  process(message):
    responses = []

    for manager in managers:
      breaker = circuit_breakers[manager.domain]

      if breaker.is_open():
        # Skip failed manager
        continue

      try:
        response = manager.process(message)
        responses.append(response)
        breaker.record_success()
      except Error:
        breaker.record_failure()

    return synthesize_partial(responses)
}
```

---

## Scaling Patterns

### Pattern 1: Load Balancing

```
Integrator {
  manager_pools: map<domain, list<ExpertManager>>

  select_manager(domain):
    pool = manager_pools[domain]
    return load_balancer.select(pool)
}
```

### Pattern 2: Sharding

```
Integrator {
  shard_managers: list<ExpertManager>

  select_manager(message):
    shard_key = hash(message.user_id)
    shard_index = shard_key % len(shard_managers)
    return shard_managers[shard_index]
}
```

---

## Testing

```
test_integrator_parallel():
  integrator = create_integrator([manager1, manager2])
  message = create_message("test")

  response = integrator.process(message)

  assert response.managers_used == 2

test_integrator_timeout():
  slow_manager = create_slow_manager(delay=10s)
  integrator = create_integrator([slow_manager], timeout=1s)

  response = integrator.process(message)

  assert response.partial == True
```

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
