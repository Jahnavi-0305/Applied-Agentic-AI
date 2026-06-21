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
