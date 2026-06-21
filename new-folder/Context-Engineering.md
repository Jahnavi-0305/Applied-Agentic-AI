### Context Engineering

**What it is:**
Context engineering = **deciding what information to put
in the prompt window** at each step of the agent's work.

Not just writing good prompts (that's prompt engineering).
This is about **dynamically assembling** the right mix of:
- 📝 Current user message
- 🧠 Relevant memory / past conversation summary
- 📚 Retrieved knowledge (from RAG / vector DB)
- ⚙️ System instructions (agent's role and rules)
- 🔧 Tool results from earlier steps in the workflow

**Simple Analogy 🎒:**
Imagine you're going to an exam.
You can only carry a small bag (token limit).
Context engineering = choosing **which notes to pack**
so you perform best — not stuffing everything in.

---

**Why it matters:**
The same LLM performs completely differently based on
what context you give it.

> ✅ Right context → accurate, coherent, useful response
> ❌ Wrong/messy context → confused, off-topic, wasted tokens

---

**4 Core Practices (MUST REMEMBER):**

1. **Prioritize Relevance**
   Only include the most useful information.
   Don't dump large blocks of text — retrieve only
   what's needed for THIS step.

2. **Maintain Clarity**
   Use structured formatting and schemas like
   **MCP (Model Context Protocol)** to pass state
   and knowledge in a predictable, clean way.

3. **Use Summarization**
   Compress long conversation history into short
   summaries — keep the key details, drop the rest.
   Saves tokens without losing important context.

4. **Assemble Dynamically**
   Rebuild the context fresh at **every step** of the
   workflow — based on current goal, current stage,
   and current user input. Don't reuse stale context.

---

**Simple vs Complex Context:**

| System | Context Contains |
|---|---|
| Simple chatbot | System prompt + latest user message |
| Multi-step agent | System prompt + user message + memory summary + RAG results + previous tool outputs |

---

**The Golden Rule:**
> Every piece of context you add must **earn its place**.
> If it doesn't help the model perform better at THIS
> step → leave it out.

---

**Context Engineering vs Prompt Engineering:**

| | Prompt Engineering | Context Engineering |
|---|---|---|
| Focus | Writing good instructions | Assembling the right information |
| Static or Dynamic | Usually static | Always dynamic |
| Scope | One prompt | Entire agent workflow |

---

**Why this makes you a better AI engineer:**
Most junior engineers focus only on the model.
Senior AI engineers know that **context quality is what
separates good agents from great ones.**
Even a weaker model performs well with great context.
Even the best model fails with poor context.


## Knowledge & Memory

**Knowledge** = external facts pulled via RAG
(docs, catalogs, logs)

**Memory** = agent's own history
(past messages, tool outputs, session state)

> Memory is WHERE knowledge is stored.
> Context Engineering is HOW it's used.

# Context Window

Context Window
│
├── Input (what goes IN to the model)
│   ├── System prompt ("you are Perplexity...")
│   ├── Your message 1
│   ├── My reply 1
│   ├── Your message 2
│   ├── My reply 2
│   └── ... entire conversation history
│
└── Output (what comes OUT)
    └── My next reply

**Context Window** = the whiteboard the LLM reads
every time you call it. Contains everything:
system prompt + history + current message.

# Foundational Memory — Rolling Context Window

**Rolling Context Window** = as conversation grows,
keep only the MOST RECENT messages.
Oldest messages get ejected automatically (FIFO).

**Problem:** Important info from early in the
conversation gets lost forever once ejected.

**Pro tip:** Place the most important context
**near the END of the prompt** — LLMs pay more
attention to recent content.


