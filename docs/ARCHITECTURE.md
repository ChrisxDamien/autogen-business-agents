# Architecture Overview

## Design Principles

This project follows a few key principles:

### 1. Local-First
Everything runs on your machine by default. No API costs, no rate limits, no data leaving your computer. You can optionally connect to cloud LLMs if needed.

### 2. Crew-Based Architecture
Each "agent system" is actually a **crew** of specialized agents working together:

```
User Request → Crew Orchestrator → [Agent 1] → [Agent 2] → [Agent 3] → Final Output
```

This mirrors how real teams work. A researcher gathers info, an analyst makes sense of it, a writer packages it.

### 3. Tool Augmentation
Agents are only as good as their tools. Each agent has access to specific tools that extend their capabilities:

- **Search Tools**: Web search, company lookup, people search
- **Processing Tools**: Summarizers, formatters, calculators
- **Integration Tools**: (Future) CRM, calendar, email

### 4. Extensible Design
Adding a new agent system should be straightforward:

1. Create agent definitions
2. Define their tools
3. Create tasks that chain them together
4. Wrap in a simple function API

---

## Component Deep Dive

### Configs (`configs/`)

**models.py**
Handles LLM provider switching. Supports:
- Ollama (default, free)
- OpenAI
- Groq

Pattern:
```python
from configs.models import get_llm

llm = get_llm()  # Returns configured LLM based on .env
```

### Tools (`tools/`)

Tools give agents capabilities beyond text generation.

**search.py**
- `web_search`: DuckDuckGo search (free, no API key)
- `linkedin_search`: People-focused search
- `company_search`: Company-focused search

**formatters.py**
- `format_meeting_agenda`: Structured agenda output
- `format_briefing`: Executive briefing format

Adding a new tool:
```python
from crewai.tools import tool

@tool("My Tool Name")
def my_tool(arg1: str, arg2: str) -> str:
    """Tool description that helps the agent decide when to use it."""
    # Implementation
    return result
```

### Agents (`agents/`)

Each file in `agents/` defines a complete crew for a specific use case.

**meeting_prep.py**
A crew of 3 agents:
1. **Researcher**: Gathers background info using search tools
2. **Strategist**: Analyzes research, identifies opportunities
3. **Planner**: Creates formatted prep document

The `prepare_for_meeting()` function orchestrates the crew:
```python
result = prepare_for_meeting(
    meeting_title="...",
    attendees=["..."],
    context="...",
    your_goals="...",
)
```

---

## Data Flow

```
┌──────────────┐
│ User Input   │
│ - Meeting    │
│ - Attendees  │
│ - Context    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│            CREW ORCHESTRATOR              │
│  - Sequences tasks                        │
│  - Passes context between agents          │
└──────────────────┬───────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐   ┌──────────┐   ┌─────────┐
│Research│──►│ Strategy │──►│ Planning│
│ Agent  │   │  Agent   │   │  Agent  │
└───┬────┘   └────┬─────┘   └────┬────┘
    │             │              │
    ▼             ▼              ▼
┌────────┐   ┌──────────┐   ┌─────────┐
│ Search │   │ Analysis │   │ Format  │
│ Tools  │   │  (LLM)   │   │ Tools   │
└────────┘   └──────────┘   └─────────┘
                   │
                   ▼
          ┌───────────────┐
          │ Final Output  │
          │ Meeting Prep  │
          │   Document    │
          └───────────────┘
```

---

## Adding New Agent Crews

### Step 1: Define Agents

```python
from crewai import Agent
from configs.models import get_llm

researcher = Agent(
    role="Your Role Name",
    goal="What this agent tries to achieve",
    backstory="Context that shapes behavior",
    tools=[tool1, tool2],
    llm=get_llm(),
)
```

### Step 2: Define Tasks

```python
from crewai import Task

task = Task(
    description="Detailed instructions for the task",
    expected_output="What good output looks like",
    agent=researcher,
)
```

### Step 3: Create Crew

```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential,  # or Process.hierarchical
)

result = crew.kickoff()
```

### Step 4: Wrap in Function

```python
def your_function(input1: str, input2: str) -> str:
    # Create agents
    # Create tasks
    # Create crew
    result = crew.kickoff()
    return result
```

---

## Error Handling

The codebase follows these error handling patterns:

1. **Tool Errors**: Tools catch exceptions and return error strings (agents can reason about failures)
2. **LLM Errors**: Bubbled up to user with troubleshooting tips
3. **Config Errors**: Fail fast with clear messages

---

## Testing

(Coming soon)

For now, test manually:
```bash
python examples/meeting_prep_example.py
```

---

## Future Architecture

### Planned Additions

1. **Memory Layer**: Allow agents to remember context across runs
2. **Async Execution**: Parallel agent execution where dependencies allow
3. **Streaming Output**: Real-time output as agents work
4. **Caching**: Cache search results and intermediate outputs
5. **Observability**: Structured logging for debugging agent behavior
