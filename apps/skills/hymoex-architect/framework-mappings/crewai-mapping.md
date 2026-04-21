# CrewAI + Hymoex Mapping

## Conceptual Mapping

| CrewAI | Hymoex |
|--------|--------|
| `Crew` | Manager |
| `Agent` | Expert |
| `Task` | Message |
| `Process` | Coordination Strategy |

## Approach: Think Hymoex Over CrewAI

```python
from crewai import Agent, Crew, Task

# Your CrewAI code (conceptual Hymoex mapping)
researcher = Agent(role="Researcher")  # = Hymoex Expert
writer = Agent(role="Writer")          # = Hymoex Expert

crew = Crew(agents=[researcher, writer])  # = Hymoex Manager

# Crew.kickoff() = Manager.process()
```

**Recommendation:** Keep CrewAI if you like its agent framework. Think in Hymoex terms for architecture.

---

**Document Version:** 1.0.0
