Here you go — beginner-friendly, ready to copy-paste:

***

## Tool Use Configuration

### Tool Choice Parameter — 3 Modes

| Mode | Behavior | When to use |
|------|----------|-------------|
| `auto` | Model decides whether to call a tool | General use, flexible |
| `required` | Model MUST call at least one tool | When tool output is essential |
| `none` | No tools allowed | Testing, controlled outputs |

***

### When Tools Fail — 4-Step Response

**1. Validate First**
Before doing anything, check if the output is correct.
Think of it like checking your food order before leaving the restaurant — wrong item? Fix it now, not later.
- Use **Pydantic or JSON Schema** to check the structure automatically

**2. Retry Intelligently — What is Exponential Backoff?**
Sometimes an API fails just because it was busy for a second. So you retry — but you wait a little longer each time so you don't spam it:
```
1st retry → wait 1 second
2nd retry → wait 2 seconds
3rd retry → wait 4 seconds
4th retry → wait 8 seconds
```
This is **exponential backoff** — waiting longer and longer between each retry.
Also: only re-run the broken part, not the whole conversation from scratch.

**3. Fallback Gracefully**
If retrying still doesn't work, don't crash — have a backup plan:
- Switch to a different model or service
- Ask the user to clarify their request
- Return a safe default answer like *"Sorry, I couldn't complete that right now."*

**4. 📋 Log Everything**
Write down every step — what the user asked, which tool was called, what went wrong, how many retries happened.
Think of it like a **black box recorder on a plane** — if something crashes, you can go back and see exactly what happened.
This is called **observability**.

***

### One Line to Remember

> **Validate → Retry → Fallback → Log.** This is what separates a toy agent from a production-grade agent. 
