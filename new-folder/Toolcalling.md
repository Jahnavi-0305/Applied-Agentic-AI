BASIC LANGCHAIN TOOL DEFINING:

# Any function you write yourself with @tool = local tool.


from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# ============================================
# STEP 1: Define your tools
# ============================================

@tool
def add_numbers(x: int, y: int) -> int:
    """Adds two numbers and returns the sum."""
    return x + y

@tool
def search_web(query: str) -> str:
    """Searches the web for information."""
    return f"Results for: {query}"  # pretend this calls a real API

# ============================================
# STEP 2: Create LLM and bind both tools
# ============================================

llm = ChatOpenAI(model_name="gpt-4o")
llm_with_tools = llm.bind_tools([add_numbers, search_web])

# tools_map so we can look up tools by name
tools_map = {
    "add_numbers": add_numbers,
    "search_web": search_web
}

# ============================================
# STEP 3: Send a message
# ============================================

messages = [HumanMessage(content="What is 5 + 3?")]
response = llm_with_tools.invoke(messages)

# LLM looks at both tools and picks add_numbers
# because the message is about math

# ============================================
# STEP 4: For loop runs whatever tool LLM picked
# ============================================

messages.append(response)  # add LLM's tool request to history

for tool_call in response.tool_calls:
    print(f"LLM picked: {tool_call['name']}")  # "add_numbers"
    print(f"With args: {tool_call['args']}")    # {"x": 5, "y": 3}

    result = tools_map[tool_call["name"]].invoke(tool_call)
    print(f"Result: {result}")                  # 8

    # Add result back to messages
    messages.append(ToolMessage(
        content=str(result),
        tool_call_id=tool_call["id"]
    ))

# ============================================
# STEP 5: Call LLM again with the tool result
# ============================================

final_response = llm_with_tools.invoke(messages)
print(final_response.content)  # "5 + 3 equals 8"


