# Basic LangChain Tool Definition

This example demonstrates how to:

1. Define custom tools using `@tool`
2. Bind tools to an LLM
3. Let the LLM choose the appropriate tool
4. Execute the selected tool
5. Return the tool result back to the LLM for a final answer

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

This pattern forms the foundation for building LangChain agents and tool-using AI applications.
