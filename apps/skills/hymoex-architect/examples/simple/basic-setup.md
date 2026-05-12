# Basic Setup Examples

**Purpose:** Simple examples to get started with Hymoex patterns.

---

## Example 1: Minimal One-Line MoE

**Use Case:** Customer support with 2 domains (technical, billing)

**Architecture:**
```
Manager → [Technical Expert, Billing Expert]
```

**Pseudocode:**
```
# Define Message
Message {
  content: string
  domain: string
}

# Define Expert Interface
Expert {
  domain: string
  process(message) -> response
}

# Technical Expert
TechnicalExpert implements Expert {
  domain = "technical"

  process(message):
    # Handle technical questions
    return "Technical solution: " + solve_technical(message.content)
}

# Billing Expert
BillingExpert implements Expert {
  domain = "billing"

  process(message):
    # Handle billing questions
    return "Billing info: " + lookup_billing(message.content)
}

# Manager
Manager {
  experts = [TechnicalExpert(), BillingExpert()]

  process(message):
    # Simple routing
    for expert in experts:
      if expert.domain == message.domain:
        return expert.process(message)

    # Default to first expert
    return experts[0].process(message)
}

# Usage
manager = Manager()
message = Message(content="How do I reset password?", domain="technical")
response = manager.process(message)
```

---

## Example 2: Research & Writing Pipeline

**Use Case:** Content creation (research → write)

**Architecture:**
```
Manager → Supervisor → [Research Expert → Writing Expert]
```

**Pseudocode:**
```
# Research Expert
ResearchExpert {
  process(query):
    results = search_web(query)
    return summarize(results)
}

# Writing Expert
WritingExpert {
  process(research):
    outline = create_outline(research)
    article = write_article(outline)
    return article
}

# Supervisor (Sequential Strategy)
Supervisor {
  experts = [ResearchExpert(), WritingExpert()]

  process(message, strategy="sequential"):
    result = message.content

    for expert in experts:
      result = expert.process(result)

    return result
}

# Manager
Manager {
  supervisor = Supervisor()

  process(message):
    return supervisor.process(message, strategy="sequential")
}

# Usage
manager = Manager()
message = Message(content="Write article about AI")
article = manager.process(message)
```

---

## Example 3: Parallel Research

**Use Case:** Comprehensive research from multiple sources

**Architecture:**
```
Manager → Supervisor → [Web Expert, Academic Expert, News Expert] (parallel)
```

**Pseudocode:**
```
# Experts
WebExpert {
  process(query):
    return search_web(query)
}

AcademicExpert {
  process(query):
    return search_papers(query)
}

NewsExpert {
  process(query):
    return search_news(query)
}

# Supervisor (Parallel Strategy)
Supervisor {
  experts = [WebExpert(), AcademicExpert(), NewsExpert()]

  process(message, strategy="parallel"):
    results = []

    # Execute all in parallel
    for expert in experts concurrently:
      result = expert.process(message.content)
      results.append(result)

    # Aggregate
    return combine_all(results)
}

# Manager
Manager {
  supervisor = Supervisor()

  process(message):
    return supervisor.process(message, strategy="parallel")
}
```

---

## Example 4: With Error Handling

**Pseudocode:**
```
Manager {
  experts = [Expert1(), Expert2(), Expert3()]

  process(message):
    try:
      expert = select_expert(message)
      return expert.process(message)

    except ExpertNotFoundError:
      return "No expert available for this request"

    except ExpertFailureError as e:
      # Try fallback
      return fallback_expert.process(message)

    except Exception as e:
      # Log and return error
      log_error(e)
      return "System error occurred"
}
```

---

## Example 5: With Caching

**Pseudocode:**
```
Manager {
  experts = [Expert1(), Expert2()]
  cache = Cache()

  process(message):
    # Check cache
    cache_key = hash(message.content)
    if cache.has(cache_key):
      return cache.get(cache_key)

    # Process
    expert = select_expert(message)
    response = expert.process(message)

    # Cache result
    cache.set(cache_key, response, ttl=3600)

    return response
}
```

---

## Testing Examples

```
# Test Expert
test_expert_processes_message():
  expert = TechnicalExpert()
  message = Message(content="test", domain="technical")

  response = expert.process(message)

  assert response is not None
  assert "technical" in response.lower()

# Test Manager Routing
test_manager_routes_correctly():
  manager = Manager()
  tech_message = Message(content="technical issue", domain="technical")

  response = manager.process(tech_message)

  assert "technical" in response.lower()

# Test Error Handling
test_manager_handles_errors():
  manager = Manager()
  invalid_message = Message(content="test", domain="unknown")

  response = manager.process(invalid_message)

  assert response is not None  # Should not crash
```

---

**Document Version:** 1.0.0
**Last Updated:** 2026-02-12
