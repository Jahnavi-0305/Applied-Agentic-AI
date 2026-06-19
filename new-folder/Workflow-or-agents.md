***

## Section 1: When to Just Use Plain Code (No AI at All)

**Simple version:**

Sometimes AI is total overkill. Use plain code when:

- **The input is always the same** — like a log file that always looks like `2026-06-19 12:00:00 - Error`. A simple Python regex handles this in 2 lines. No LLM needed.
- **Speed is critical** — if your system needs to respond in milliseconds (like a sensor in a car or medical device), you literally don't have time for an API call to OpenAI.
- **The rules must be 100% explainable** — hospitals, airplanes, banks sometimes legally require that every decision can be audited and explained step by step. An AI "black box" that says "I think so" doesn't pass that audit.

> **Rule of thumb:** If you already know every possible input AND every possible output — just write the code. Don't make it complicated.

***

## Section 2: When to Use a Workflow (Like Airflow or AWS Step Functions)

**Simple version:**

A workflow is like a **flowchart with fixed boxes and arrows**. You know every step in advance, and you know every possible decision branch.

Example: Invoice processing
```
Invoice arrives
    ↓
Parse the invoice
    ↓
Does it match our records? 
  YES → Approve automatically
  NO  → Send to human for review
```

You don't need an AI to do this. Every possible path is already mapped out. Tools like **Airflow** (which you've used!) or **AWS Step Functions** are perfect here.

> **Rule of thumb:** If you can draw the entire flowchart on a whiteboard and cover every case — use a workflow, not an agent.

***

## Section 3: When to Use a RAG System (Chatbot + Documents)

**Simple version:**

RAG = *"let users ask questions about your documents."*

Example: A company has 500 internal IT guides. An employee asks: *"How do I reset my VPN?"*

The RAG system:
1. Searches the 500 documents for relevant ones
2. Pulls out the right paragraphs
3. Generates a clean answer

That's it. **It answers questions. It doesn't take actions.**

It won't automatically create a support ticket, won't call IT, won't schedule a callback. It just surfaces information. Simple, cheap, effective — for the right use case.

> **Rule of thumb:** If the job is *"answer questions from documents"* — RAG is enough. Don't build an agent.

***

## Section 4: When to Use a Full Agent

**Simple version:**

Now we reach the point where everything else breaks down. Use an agent when:

- **Inputs are unpredictable** — like customer emails. One says *"my laptop battery is swelling"*, next says *"I was billed for something I didn't order."* You can't write a flowchart for this. Too many possibilities.
- **Multiple steps needed dynamically** — the agent needs to figure out the steps *on its own*, not follow a script
- **Things run in parallel** — like a security agent that simultaneously checks threat databases, scans network logs, AND analyzes suspicious files — all at the same time
- **The system needs to self-improve** — agents can learn from feedback loops over time

> **Rule of thumb:** If the inputs are messy, unpredictable, and require real thinking — use an agent.

***

## The Big Decision Table (The Most Important Thing in This Section)

| Your Situation | Best Solution |
|---|---|
| Fixed inputs, fixed outputs, no thinking needed | **Plain code / script** |
| Known steps, known branches, needs audit trail | **Workflow (Airflow, Step Functions)** |
| Users asking questions about documents | **RAG system** |
| Messy inputs, dynamic decisions, parallel tasks | **Autonomous Agent** |

***

## The 4 Questions to Ask Yourself

When deciding, just ask these 4 questions:

1. **Are my inputs messy and unpredictable?**
2. **Do I need multi-step planning that figures itself out?**
3. **Does the system need to improve itself over time?**
4. **Can I tolerate the cost and maintenance of running an LLM?**

If most answers are **YES** → build an agent.
If most answers are **NO** → use something simpler.

***

## One Line Summary of the Whole Section

> **Don't use a sledgehammer to crack a nut. Use the simplest tool that solves the problem.**

Plain code → Workflow → RAG → Agent. Each level is more powerful but also more expensive and harder to maintain. Pick the right level for your problem. That's the whole point. 




## IMP UI POINTS:

An **autonomy slider** is a design pattern that lets users control how much they trust an AI agent by choosing between three modes. In **Manual mode**, the human does everything and the agent stays silent. In **Ask mode**, the agent suggests actions but the human must approve each one before anything happens — like GitHub Copilot suggesting code that you accept by pressing Tab. In **Agent mode**, the agent acts on its own and only notifies the human afterward — like an AI that automatically fixes bugs without asking. The key insight is that users should never be forced into full autonomy from day one. Trust is built gradually — users start in Ask mode, see that the agent makes good decisions, and then choose to give it more control over time. Without this slider, an agent either feels useless because it does nothing, or feels scary because it does too much without permission.



When building an AI agent, users often don't know what the agent can do — unlike a normal app where buttons and menus make everything visible. Your job as a designer and engineer is to make the agent's capabilities obvious without overwhelming the user. You do this in simple ways: add suggested action buttons below the chat input (like "Track Order" or "Generate Summary"), show a capability menu or sidebar listing what the agent can do, and use dynamic suggestions that appear as the user types (like how Google autocompletes your search). When a user asks for something the agent can't do, don't just say "I can't do that" — instead say "I can't process payments, but I can update your billing preferences" — always offer an alternative. Most importantly, don't dump every feature on the user at once. Use progressive disclosure — show the basics first, reveal advanced features only as the user gets comfortable. The whole goal is simple: turn the agent from a confusing black box into something that feels like a helpful, transparent assistant that guides you rather than confuses you.


**FAILING GRAFULLY:**

Every AI agent will fail at some point — that's guaranteed. What matters is how it fails. A well-designed agent never just crashes or returns a confusing error. Instead it does four things: acknowledge the failure honestly ("I couldn't find what you're looking for"), explain briefly why it failed, offer a next step ("Would you like me to escalate to a human?"), and use empathetic language that feels human, not robotic. In multi-step tasks, the agent should save progress so the user doesn't have to start over from scratch — this is directly connected to LangGraph's checkpointing feature you already learned. If the agent repeatedly fails to understand voice input, it should switch modalities — offer text instead. Most importantly, every failure should be logged so engineers can analyze patterns and fix recurring issues over time. The goal is simple: even when the agent fails, the user should still feel helped, not abandoned.



