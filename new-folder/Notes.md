# Building Applications with AI Agents

## What is an Agent?

An **AI agent** is different from a traditional AI model.

A model that only generates text is not really an agent. An agent is something that can **make decisions and take actions on its own**.

Think of a **travel agent**:

* A travel agent does not just tell you how to book a flight.
* A travel agent actually books the flight for you.

### Traditional AI

**User:**

> Book me a flight to New York tomorrow.

**Old AI Response:**

> Sure! Here's how you could book a flight...

The AI only generates text. It does not perform any action.

### AI Agent

**User:**

> Book me a flight to New York tomorrow.

**Agent's Decision:**

```text
Call function:
book_flight(
    destination="New York",
    date="tomorrow"
)
```

The system then executes the function and books the flight.

---

## The Key Unlock for Agents

The magic behind agents is:

### From Talking → To Doing

Instead of only generating text, the LLM can:

1. Know what tools are available
2. Decide which tool to use
3. Fill in the required parameters
4. Execute the tool
5. Use the result

Example tools:

```text
search_google()
send_email()
book_flight()
```

The LLM chooses the correct tool and provides the inputs.

---

## Structured Function Signatures

This simply means the AI knows:

* What tools exist
* What each tool does
* What parameters each tool requires

Example:

```python
book_flight(
    destination: str,
    date: str
)
```

The LLM understands:

* Function = `book_flight`
* Parameters = `destination`, `date`

It fills them automatically and calls the tool.

This is what allows AI to interact with real-world systems.

---

# Why Do We Need an Orchestrator?

An **orchestration framework** coordinates:

* The LLM
* The tools
* The workflow
* The execution order

Examples:

* LangGraph
* LangChain
* CrewAI
* AutoGen

### Restaurant Analogy

#### LLM = Head Chef

Decides:

> What should be cooked?

#### Tools = Kitchen Equipment

Examples:

* Oven
* Knife
* Stove

#### Orchestrator = Kitchen Manager

Makes sure:

* The right tool is used
* At the right time
* In the right order

```text
LLM (Brain)
      ↓
Orchestrator
      ↓
Tools
      ↓
Actions
```

---

# MCP and Agent-to-Agent Protocols

## MCP (Model Context Protocol)

MCP is a standard way for agents to access:

* APIs
* Databases
* External tools
* Internet resources

using a common interface.

---

## Agent-to-Agent Protocol

Agents can communicate and collaborate.

Example:

### Agent 1

Researches information.

### Agent 2

Writes the report.

### Agent 3

Sends the email.

```text
Research Agent
       ↓
Writing Agent
       ↓
Email Agent
```

Each agent specializes in a specific task.

---

# How Do Agents Actually Call Tools?

Question:

> If an agent can search Google, send emails, or book flights, does it use FastAPI, REST APIs, Graph APIs, etc.?

### Short Answer

Yes.

But not directly.

---

## The Three Layers

```text
Agent (LangGraph Node)
          ↓

Tool Function (Python Function)
          ↓

Real API (REST API / Graph API / SDK)
```

The agent calls a tool function.

The tool function then calls the actual API.

The agent never talks directly to the API.

It only knows:

```text
search_web()
send_email()
book_flight()
```

---

## Example

Agent calls:

```python
search_web("latest AI news")
```

Inside the tool:

```python
requests.get(...)
```

A REST API request is made.

Results are returned back to the agent.

---

## Real Architecture

```text
User
 ↓

Agent (LLM)
 ↓

Tool Function
 ↓

REST API / Graph API / SDK
 ↓

External Service
```

---

## Common Examples

| Agent Wants To Do  | Tool Function             | API Behind It                 |
| ------------------ | ------------------------- | ----------------------------- |
| Search the web     | `search_web(query)`       | Google Search REST API        |
| Send email         | `send_email(to, body)`    | Gmail REST API / SendGrid     |
| Book flight        | `book_flight(dest, date)` | Amadeus / Skyscanner API      |
| Read database      | `query_db(sql)`           | Database / REST API           |
| Call another agent | `call_agent(task)`        | MCP / Agent-to-Agent Protocol |

---

## Important Takeaway

The agent does not care whether the tool uses:

* REST API
* Graph API
* SDK

It only knows:

```text
Tool Name
↓
Parameters
↓
Result
```

This is called **tool abstraction**.

The LLM has evolved from:

```text
Talking
```

to

```text
Taking Actions
```


Yes, exactly! That's literally it. 😄

The whole concept boils down to **3 keywords**:

***

```python
async def my_function():   # 👈 "this function is async"
    await some_api_call()  # 👈 "wait for this, but don't block others"

asyncio.gather(f1(), f2()) # 👈 "run both at the same time"
```

***

That's the **entire secret** of asynchronous programming.

- Write `async def` instead of `def` → done, your function is now async
- Write `await` before any slow operation (API call, DB call, file read) → done, it won't block
- Use `asyncio.gather()` when you want multiple things at the same time → done, they run in parallel

The book makes it sound complicated with big words like *"asynchronous operation"* and *"parallel execution"* and *"reducing idle time"* — but the actual code change is just:

```python
# Before (sync)
def fetch_email():

# After (async)
async def fetch_email():
```

That's genuinely it. One word changes everything. 🎯
