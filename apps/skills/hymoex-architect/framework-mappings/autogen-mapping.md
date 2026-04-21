# AutoGen + Hymoex Mapping

## Conceptual Mapping

| AutoGen | Hymoex |
|---------|--------|
| `ConversableAgent` | Expert |
| `GroupChat` | Supervisor |
| `GroupChatManager` | Manager |

## Approach: Map AutoGen Patterns to Hymoex

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager

# AutoGen agents = Hymoex Experts
researcher = ConversableAgent(name="Researcher")  # Expert
writer = ConversableAgent(name="Writer")          # Expert

# GroupChat = Hymoex Supervisor (routing)
group_chat = GroupChat(agents=[researcher, writer])

# GroupChatManager = Hymoex Manager (orchestration)
manager = GroupChatManager(groupchat=group_chat)
```

**Recommendation:** AutoGen's conversational model maps naturally to Hymoex. Use Hymoex thinking for structure.

---

**Document Version:** 1.0.0
