### LangGraph Core Pattern (Always Remember This)

**Step 1 — Define State**
```python
class MessagesState(TypedDict):
    messages: list  # state = dictionary flowing through graph
```

**Step 2 — Define Nodes (functions)**
```python
def call_model(state):
    response = llm.invoke(state["messages"])
    return {"messages": response}  # always return updated state
```

**Step 3 — Build Graph**
```python
graph = StateGraph(MessagesState)
graph.add_node("call_model", call_model)
graph.add_edge(START, "call_model")
graph.add_edge("call_model", END)
graph = graph.compile()
```

**Step 4 — Run Graph**
```python
graph.invoke({"messages": [user_message]})  # run once
graph.stream({"messages": [user_message]})  # stream output
```

**The 4 steps always stay the same:**
1. Define State (TypedDict)
2. Define Nodes (functions)
3. Build + compile graph
4. invoke() or stream()

What is graph.stream() vs graph.invoke()?
invoke() = run and wait for the full final answer

stream() = run and get partial outputs word by word as they're generated — like how ChatGPT types out responses live
