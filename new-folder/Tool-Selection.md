| Agent Type          | One-Line Summary                                         |
| ------------------- | -------------------------------------------------------- |
| Planner-Executor    | Plans all steps first, then executes one by one          |
| Query Decomposition | Breaks one big question into smaller sub-questions       |
| Reflection Agent    | After answering, checks its own answer and improves it   |
| Deep Research Agent | Multi-stage investigation — searches, reads, synthesizes |



### Tool Selection

#### 1. Standard Tool Selection

**What it is:**
The simplest way for an agent to pick a tool.
You give the AI model a list of tools with descriptions, and it reads them and picks the most suitable one for the user's query.

**Simple Example:**
Imagine you have 3 tools:
- `calculate_sum` → "Returns the sum of two numbers"
- `get_weather` → "Returns current weather for a city"
- `search_web` → "Searches the internet for information"

User asks: *"What is 5 + 3?"*
The model reads all descriptions → picks `calculate_sum`. That's standard tool selection.

**How to write good tool descriptions:**
1. **Give a clear name** → `calculate_sum` not `process_numbers`
2. **One-sentence summary** → "Returns the sum of two numbers"
3. **Show an example** → Input: `x=5, y=3` → Output: `8`
4. **Add constraints** → "x and y must be integers between 0 and 1000"

**Pros:**
- Easy to implement
- No extra training or setup needed
- Can use few-shot examples to improve accuracy

**Cons:**
- Adds latency (requires an extra model call — adds seconds)
- Breaks down when you have many tools with similar descriptions
  - Example: `calculate_sum` and `evaluate_formula` both sound like math tools → agent gets confused

**When to use:**
Small number of tools (under ~10–15)
Not ideal for large tool sets with overlapping descriptions


#### Standard Tool Selection — Code Pattern to Remember

```python
# Step 1 — Define a tool with @tool decorator + clear docstring
@tool
def tool_name(input: str) -> str:
    """One clear description of what this tool does."""
    # call an API or do something
    return result

# Step 2 — Bind tools to your LLM
llm = ChatOpenAI(model_name="gpt-4o")
llm_with_tools = llm.bind_tools([tool1, tool2, tool3])

# Step 3 — Invoke and let the model pick the right tool
ai_msg = llm_with_tools.invoke([HumanMessage("user query")])
```

**The 3 steps always stay the same:**
1. `@tool` → define your tool with a good description
2. `bind_tools([...])` → give the tools to your LLM
3. `invoke()` → LLM reads descriptions and picks the right one



#### 2. Semantic Tool Selection

**What it is:**
Instead of giving ALL tools to the LLM and letting it pick,
you first use **embeddings + vector search** to find the top
relevant tools, THEN let the LLM pick from that small set.

**Simple Example:**
You have 50 tools. User asks: *"What is 5 + 3?"*
- Embed the query → search vector DB → top 2 tools returned:
  `calculate_sum`, `evaluate_formula`
- LLM picks from just these 2 → much faster and accurate

vs Standard Tool Selection where LLM reads all 50 tools 

**How it works (4 steps):**
1. **Embed all tool descriptions** → store in vector DB (FAISS, Pinecone, etc.) — done once ahead of time
2. **At runtime** → embed the user query using same model
3. **Vector search** → find top-K most similar tools
4. **LLM picks** from that small shortlist → invokes the tool

**Code Pattern to Remember:**
```python
# Step 1 — Embed tools once and store in FAISS
embeddings.embed_text(tool_description) → store in FAISS index

# Step 2 — At runtime, embed the query
query_embedding = embeddings.embed_text(user_query)

# Step 3 — Search for top tools
D, I = index.search(query_embedding, top_k=1)

# Step 4 — LLM picks and invokes
llm_with_tools.invoke(selected_tools)
```

**Pros:**
- Faster than standard tool selection
- Scales to large tool sets (50, 100, 500+ tools)
- Most recommended approach for most use cases

**Cons:**
- Slightly more setup (need vector DB + embedding model)

**Standard vs Semantic — Quick Difference:**
| | Standard | Semantic |
|---|---|---|
| Tools given to LLM | All tools | Top-K only |
| Scales to many tools |  No | Yes |
| Setup complexity | Simple | Moderate |
| Speed | Slower | Faster |


#### 3. Hierarchical Tool Selection

**What it is:**
Tools are organized into **groups/categories** first.
Selection happens in **2 stages** — pick the group, then
pick the tool inside that group.

**Simple Example:**
You have 100 tools organized into 3 groups:
- **Computation** → `calculate_sum`, `wolfram_alpha`
- **Automation** → `zapier_webhook`, `run_script`
- **Communication** → `send_slack`, `send_email`

User asks: *"Solve 2x + 3 = 7"*
- Stage 1: LLM picks group → **Computation**
- Stage 2: LLM picks tool from Computation → `wolfram_alpha`

**Code Pattern to Remember:**
```python
# Stage 1 — Pick the group
selected_group = select_group_llm(query)

# Stage 2 — Pick the tool inside that group
selected_tool = select_tool_llm(query, selected_group)
```

**Pros:**
- Higher accuracy for large tool sets
- Breaks a hard problem into 2 easier ones

**Cons:**
- Slower (2 LLM calls instead of 1)
- More setup — you must manually organize and maintain groups
- Only use when you have a LOT of similar tools

---

### 🏆 Which Tool Selection to Use — Quick Guide

| Method | Use When |
|---|---|
| **Standard** | Small tool set (~10 tools), quick to build |
| **Semantic** | Most cases ✅ — scales well, fast, recommended |
| **Hierarchical** | 100+ tools that are semantically similar |

> **Most companies use Semantic Tool Selection.**
> It's the sweet spot — scalable, fast, and no manual
> grouping needed.

### Tool Execution

After a tool is selected, the LLM reads the user query and
current context to **fill in the parameters** the tool
needs (e.g. `city="Houston"`). Before calling the tool, a
**basic validator checks the inputs** — if wrong, the LLM
is asked to correct them. The tool is then **executed**
either locally (e.g. math calculation) or remotely (e.g.
weather API), with **timeout and retry logic** to handle
slow or failed responses.

# Tool Topology:

Tool Topology means "What pattern/shape does the agent use when calling multiple tools?"

Now with agents, you just give the agent a set of tools and say "here are your tools, figure it out." The agent decides the order dynamically based on the task.


#### 1. Single Tool Execution

The simplest pattern — agent picks **exactly one tool**,
fills its parameters, executes it, and uses the result to
answer the user.

**Flow:**
User query → select 1 tool(from any number of tools present it only selects one) → fill parameters → execute → respond

**When to use:** Simple, single-step tasks
(e.g. weather lookup, math calculation, web search)

> This is the foundation. All complex patterns
> (parallel, sequential) are built on top of this.


Great — you covered 3 topics. Let me break all of them down simply, then give you the notes.

***

## Parallel Execution — Simple Explanation

**One query → Multiple tools run AT THE SAME TIME**

**Example:**
User asks: *"Give me full info about patient John."*

Agent runs all these **simultaneously** 🔄:
- `get_patient_records` 
- `get_medical_history`
- `get_insurance_info`

All 3 run **at the same time** → results combined → one final answer.

**Why parallel?** Because these tools don't depend on each other. No need to wait.

***

## Chains — Simple Explanation

**One query → Tools run ONE AFTER ANOTHER (sequential)**

**Example:**
User asks: *"Search the web and then send a Slack summary."*

```
Step 1: search_web("AI news") ✅
        ↓ (result passed to next)
Step 2: summarize(result) ✅
        ↓
Step 3: send_slack(summary) ✅
```

Step 2 **cannot start** until Step 1 finishes. That's a chain.

**Your instinct was right** — yes, chains are slower because of waiting. But sometimes you HAVE to wait (you can't summarize before searching).

***

## Runnable — Simple Explanation

what **Runnable** means in LangChain:

Think of it like a **USB standard** 🔌

Every device (keyboard, mouse, phone) uses the same USB port. You don't need a different port for each device.

In LangChain, every component — prompt, model, tool, chain — uses the **same 3 methods**:
- `.invoke()` → run once
- `.batch()` → run many at once
- `.stream()` → run and get output word by word

That's all Runnable means. **Same interface for everything.**

***

````markdown
### Tool Topology (continued)

#### 2. Parallel Tool Execution

Multiple tools run **simultaneously** for one query.
Results are collected after all finish → combined into
one final response.

**When to use:** When tools are independent of each other
(e.g. fetching patient records + history + insurance at
the same time)

**How agent selects tools:**
1. Semantic search → retrieve top 5 candidate tools
2. LLM filters down → picks only necessary ones
3. All selected tools run **in parallel**
4. Results combined → final response

**Pros:** ✅ Fast — no waiting between tools
**Cons:** ❌ Complex to manage, unclear how many tools needed

---

#### 3. Chains (Sequential Execution)

Tools run **one after another** — each step depends on
the previous step's output.

**Flow:**
```
Tool 1 → output → Tool 2 → output → Tool 3 → final answer
```

**Example:**
`search_web` → `summarize` → `send_slack`
(Can't summarize before searching)

**When to use:** Step-by-step tasks where order matters
and each step feeds into the next

**Pros:** ✅ Good for linear workflows with dependencies
**Cons:** ❌ Slower (waiting at each step), errors compound
down the chain

> ⚠️ Always set a **maximum chain length** — errors
> at step 1 will affect every step after it

**LangChain LCEL (LangChain Expression Language):**
A clean syntax to build chains without boilerplate.
Every component (prompt, model, tool) is a **Runnable**
— meaning they all share the same 3 methods:
- `.invoke()` → run once
- `.batch()` → run many inputs at once
- `.stream()` → stream output word by word

---

### Parallel vs Chain — Quick Difference

| | Parallel | Chain |
|---|---|---|
| Tools run | Same time | One after another |
| Steps depend on each other | ❌ No | ✅ Yes |
| Speed | Fast | Slower |
| Use when | Independent tasks | Sequential tasks |
````

***


Great — you understood the concept correctly! Here are your notes:

***

````markdown
#### 4. Graphs (LangGraph)

**What it is:**
The most flexible pattern. Instead of linear steps (chain)
or flat parallel calls, a graph lets you **branch, merge,
and loop** based on conditions.

**Simple Example:**
User says: *"I have a billing problem."*

```
User message
      ↓
categorize_issue → "billing" or "technical"?
      ↓                        ↓
handle_invoice          handle_login
      ↓                        ↓
summarize_response ← ← ← ← ← ←
      ↓
Final answer to user
```

Different paths depending on the issue —
all paths merge back into one final response.

**Key Concepts to Remember:**
- **Node** = one step / one tool call
- **Edge** = connection between steps
- **Conditional Edge** = "go to X if condition A,
  go to Y if condition B"
- **Consolidation Edge** = multiple branches merging
  back into one node
- **State** = a dictionary passed through every node,
  updated at each step

**Pros:**
- ✅ Handles complex non-linear workflows
- ✅ Branch + merge in any pattern
- ✅ Very flexible

**Cons:**
- ❌ More LLM calls = higher cost + latency
- ❌ Risk of cycles (infinite loops) and unreachable nodes
- ❌ Harder to debug and maintain

> ⚠️ Always set `max_depth` to prevent infinite loops

---

### When to Use Which Topology

| Topology | Use When |
|---|---|
| **Single Tool** | One simple task, one tool needed |
| **Parallel** | Multiple independent tools needed at once |
| **Chain** | Steps must happen in order, each depends on previous |
| **Graph** | Complex branching + merging required |

> Start simple. Use a chain first.
> Only use a graph when you MUST branch AND merge.

---

### Code Pattern to Remember (LangGraph)

Only remember this skeleton — not the full code:

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph()

# Add nodes (each node = one function/tool)
graph.add_edge(START, node_a)

# Add conditional edges (branching)
graph.add_conditional_edges(
    node_a,
    router_function,  # decides which path
    mapping={"option1": node_b, "option2": node_c}
)

# Consolidation (merge branches back)
graph.add_edge(node_b, final_node)
graph.add_edge(node_c, final_node)

graph.add_edge(final_node, END)

# Run
result = graph.run(initial_state, max_depth=5)
```

**That's all you need.** The pattern is always:
`START → nodes → conditional edges → consolidate → END`
````

***

Remember Just This:

**Concept question:** *"What's the difference between chains and graphs?"*
> *"Chains are linear — step A feeds into step B feeds into step C. Graphs allow branching and merging — you can split into multiple paths based on conditions and consolidate results back into one response. I use LangGraph for graphs, where nodes are tool calls and edges define transitions."*

**Code question:** Only need to know `add_edge`, `add_conditional_edges`, `START`, `END`, and `max_depth`. Nothing else. 




