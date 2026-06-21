### Semantic Experience Memory

Stores ALL past interactions as embeddings.
At each new session, searches past interactions
semantically and injects the most relevant ones
into the context window.

**vs RAG:**
- RAG = retrieves from external documents
- Semantic Experience Memory = retrieves from
  the agent's own past conversations

**Result:** Agent feels personalized and adaptive
across sessions — like it "knows" the user.


User query
    ↓
Search BOTH at the same time:

┌─────────────────────┐    ┌──────────────────────────┐
│   RAG Vector DB     │    │  Experience Memory DB     │
│  (company docs,     │    │  (past conversations,     │
│   policies, FAQs)   │    │   user preferences)       │
└─────────────────────┘    └──────────────────────────┘
         ↓                            ↓
    "Refund policy                "This user
     is 30 days"                   prefers email
                                   not Slack"
              ↓              ↓
         Both results injected into context
                    ↓
                  LLM
                    ↓
         Personalized + accurate answer

> **RAG + Semantic Experience Memory Together:**
> RAG = what the company knows
> Experience Memory = what the agent remembers about YOU
> Combined = answers that are both accurate AND personalized
