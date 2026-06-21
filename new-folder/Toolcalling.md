# Basic LangChain Tool Definition

This example demonstrates how to:

1. Define custom tools using `@tool` (Any function you write yourself with @tool = local tool.)
3. Bind tools to an LLM
4. Let the LLM choose the appropriate tool
5. Execute the selected tool
6. Return the tool result back to the LLM for a final answer

---

## Imports

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
```

---

## Step 1: Define Your Tools

Any function decorated with `@tool` becomes a LangChain tool.

```python
@tool
def add_numbers(x: int, y: int) -> int:
    """Adds two numbers and returns the sum."""
    return x + y


@tool
def search_web(query: str) -> str:
    """Searches the web for information."""
    return f"Results for: {query}"  # Pretend this calls a real API
```

---

## Step 2: Create the LLM and Bind Tools

Bind all available tools to the model so it can decide which one to use.

```python
llm = ChatOpenAI(model_name="gpt-4o")

llm_with_tools = llm.bind_tools([
    add_numbers,
    search_web
])
```

Create a lookup dictionary to execute tools dynamically.

```python
tools_map = {
    "add_numbers": add_numbers,
    "search_web": search_web
}
```

---

## Step 3: Send a User Message

```python
messages = [
    HumanMessage(content="What is 5 + 3?")
]

response = llm_with_tools.invoke(messages)
```

### What Happens?

The LLM sees:

- Available tool: `add_numbers`
- Available tool: `search_web`
- User asks: `"What is 5 + 3?"`

The model determines that the math tool is the best choice and generates a tool call instead of answering directly.

---

## Step 4: Execute the Tool Selected by the LLM

Add the LLM response (containing the tool call) to conversation history.

```python
messages.append(response)
```

Execute every tool call requested by the model.

```python
for tool_call in response.tool_calls:

    print(f"LLM picked: {tool_call['name']}")
    print(f"With args: {tool_call['args']}")

    result = tools_map[tool_call["name"]].invoke(tool_call)

    print(f"Result: {result}")

    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )
    )
```

### Example Output

```text
LLM picked: add_numbers

With args:
{
    "x": 5,
    "y": 3
}

Result: 8
```

---

## Step 5: Send Tool Results Back to the LLM

Now that the tool has been executed, send the updated conversation back to the model.

```python
final_response = llm_with_tools.invoke(messages)

print(final_response.content)
```

### Output

```text
5 + 3 equals 8.
```

---

# Complete Flow Diagram

```text
User
 │
 │  "What is 5 + 3?"
 ▼
LLM + Tools
 │
 │ decides tool needed
 ▼
add_numbers(x=5, y=3)
 │
 │ returns 8
 ▼
ToolMessage(content="8")
 │
 ▼
LLM
 │
 ▼
"5 + 3 equals 8."
```

---

# Full Example

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


# ==========================
# Define Tools
# ==========================

@tool
def add_numbers(x: int, y: int) -> int:
    """Adds two numbers and returns the sum."""
    return x + y


@tool
def search_web(query: str) -> str:
    """Searches the web for information."""
    return f"Results for: {query}"


# ==========================
# Create LLM
# ==========================

llm = ChatOpenAI(model_name="gpt-4o")

llm_with_tools = llm.bind_tools([
    add_numbers,
    search_web
])

tools_map = {
    "add_numbers": add_numbers,
    "search_web": search_web
}


# ==========================
# User Message
# ==========================

messages = [
    HumanMessage(content="What is 5 + 3?")
]

response = llm_with_tools.invoke(messages)

messages.append(response)


# ==========================
# Execute Tool Calls
# ==========================

for tool_call in response.tool_calls:

    print(f"LLM picked: {tool_call['name']}")
    print(f"With args: {tool_call['args']}")

    result = tools_map[tool_call["name"]].invoke(tool_call)

    print(f"Result: {result}")

    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )
    )


# ==========================
# Final LLM Response
# ==========================

final_response = llm_with_tools.invoke(messages)

print(final_response.content)
```

---

# Key Takeaways

- `@tool` converts a Python function into a LangChain tool.
- `bind_tools()` makes tools available to the model.
- The LLM decides which tool to call based on the user's request.
- Tool calls appear in `response.tool_calls`.
- Execute the selected tool manually.
- Return results using `ToolMessage`.
- Invoke the model again to generate the final natural-language response.

# WHAT TO REMEMBER ABOUT LOCAL TOOLS

Just 3 things:

***

## What to Remember About Local Tools

**1. What they are:**
Functions YOU write with `@tool` that run on your own machine. No internet needed.

**2. When to use them:**
When the LLM is bad at something — math, dates, time zones, calendar math. Use a local tool instead of trusting the LLM to calculate.

**3. The docstring is everything:**
```python
@tool
def add_numbers(x: int, y: int) -> int:
    """Adds two integers. Use when user wants to add numbers."""
    return x + y
```
Bad docstring = LLM calls wrong tool or never calls it.
Good docstring = LLM always calls it at the right time.

***




This pattern forms the foundation for building LangChain agents and tool-using AI applications.


#API TOOLS:

No, you don't need to memorize the exact code. But you need to understand the **pattern** — because every API-based tool follows the same structure.

***

## The Pattern (This is What You Remember)

```python
import requests
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Gets current weather for a given city."""
    response = requests.get(
        "https://api.weather.com/current",   # ← external API
        params={"city": city, "key": API_KEY}
    )
    return response.json()["description"]
```

That's it. Every single API-based tool looks like this:
1. `@tool` on top
2. Good docstring
3. `requests.get()` or `requests.post()` inside
4. Return the result

***

## Local Tool vs API Tool — The Only Difference

```python
# LOCAL TOOL — runs on your machine
@tool
def add_numbers(x: int, y: int) -> int:
    """Adds two numbers."""
    return x + y          # ← pure Python, no internet

# API TOOL — calls external service
@tool
def get_weather(city: str) -> str:
    """Gets weather for a city."""
    response = requests.get("https://weather-api.com", ...)  # ← internet call
    return response.json()
```

**Same `@tool` decorator. Same docstring pattern. Only difference = internet call inside.**

***

## What to Remember for Interviews

If asked *"how do you build an API-based tool for an agent?"* say:

> *"Same as a local tool — use `@tool` decorator with a clear docstring. Inside the function, make a `requests.get()` or `requests.post()` call to the external API, parse the response, and return a clean string result back to the LLM."*

***


> **API tools = local tools + a `requests` call inside. Same pattern, just reaches out to the internet.**


# Model Context Protocol (MCP)

## What MCP Actually Is

**One sentence:** MCP is a universal plug-and-play standard so any AI agent can connect to any data source/tool without writing custom code for each one.

> 💡 **Best interview analogy:** MCP is the **USB-C port for AI** — one port, works with everything.

***

## The 2 Core Roles

| Role | What It Is | Simple Analogy |
|------|-----------|----------------|
| **MCP Server** | Wraps a data source (database, CRM, storage) and exposes methods via JSON-RPC | A waiter who knows the menu |
| **MCP Client** | The agent that sends requests and receives responses | The customer ordering food |

> The client doesn't need to know how the server works internally — just what methods it exposes.

***

## What to Remember Technically

- **JSON-RPC 2.0** over HTTPS or WebSocket — this is the "language" both sides speak
- Servers advertise their **method catalog** (list of available functions + their input/output shapes)
- The agent reads the catalog and **reasons about which method to call** and with what parameters — automatically

***

## Why It Matters

| | Before MCP | After MCP |
|--|-----------|----------|
| Integration | Write a custom adapter for every single data source | Build one MCP server per data source |
| Reusability | Brittle, hard to maintain, doesn't scale | Any agent can use it instantly |

***

## Security Gaps — Worth Mentioning in Interviews 

MCP is still maturing. Key unsolved problems:

- No standardized **authentication** solution built into the spec
- **Role-based access control** (who can call what) is still being figured out
- Risk of **malicious payload injection** when multiple agents share MCP endpoints

> Mentioning these in an interview shows senior-level thinking. 

***

## One-Paragraph Summary

> MCP = USB-C for AI. A **server** exposes tools via JSON-RPC 2.0. A **client** (agent) fetches the method catalog and calls what it needs. No custom adapters. Any agent, any tool, same protocol. **Security is the current weak spot.**

# CODE

Remember These 4 Things Only

### 1. The Pattern (Always the same)
```
Create client → get_tools() → pick tool → arun()
```
Every MCP implementation follows this exact flow. Period.

### 2. Two Transport Types
| Transport | When used |
|-----------|-----------|
| `stdio` | Server runs **locally** as a subprocess |
| `streamable_http` | Server runs **remotely** over HTTP |

### 3. Multi-Server is Normal
In real companies, one agent connects to **many servers** — databases, CRMs, internal APIs — all in one `MultiServerMCPClient({...})` dictionary. Each key is just a name you give the server.

### 4. Always Async
`get_tools()` and `arun()` are always **async/await** because they're network calls.
Because Without async, if user 1, 2, 3 are calling an API. User 1 faces problem then User 2 and User 3 are stuck waiting for User 1's API call to finish, even though their requests have nothing to do with each other.

With async, all 3 run at the same time. If User 1's weather API fails, only User 1 gets the error message. Users 2 and 3 get their responses normally — no one else is affected. 


***

## What Changes Company to Company

Only these two things change:
- The **server names** (math, weather → orders, inventory, payments...)
- The **routing logic** (how the agent decides which tool to call)

The MCP pattern itself **never changes**. 

***

That's it. If you remember the 4-step pattern and two transports, you can work with any company's MCP setup on day one. 
