# 🤖 Business Agents

**Production-ready multi-agent systems for business automation. 100% local. Zero API costs.**

> Most AI agent tutorials cost $50+/month in API fees. This runs entirely on your machine using Ollama. Your data never leaves your computer.

---

## What's Inside

| Agent | What It Does | Status |
|-------|--------------|--------|
| 🗓️ **Meeting Prep Agent** | Researches attendees, drafts agendas, suggests talking points | ✅ Ready |
| 🔍 **Lead Research Agent** | Takes a company name, returns firmographics + key contacts | 🚧 Coming |
| 📄 **Document Q&A Agent** | Chat with your PDFs and docs using RAG | 🚧 Coming |
| ✉️ **Email Drafter Agent** | Context-aware email responses | 🚧 Coming |
| 📊 **Competitive Intel Agent** | Monitor competitors, summarize changes | 🚧 Coming |

---

## Why This Exists

I built these because:

1. **Most agent examples are toys** - They demo well but break in production
2. **API costs add up fast** - $0.01 per call × 1000 calls/day = real money
3. **Business context matters** - Generic agents don't understand your workflows

These agents are designed for **real business use cases** with proper error handling, logging, and extensibility.

---

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed locally

### 1. Clone and Install

```bash
git clone https://github.com/chris-damien/autogen-business-agents.git
cd autogen-business-agents
pip install -r requirements.txt
```

### 2. Pull a Local Model

```bash
# Recommended: Llama 3.2 (good balance of speed + quality)
ollama pull llama3.2

# Alternative: Mistral (faster, slightly less capable)
ollama pull mistral
```

### 3. Run Your First Agent

```bash
python examples/meeting_prep_example.py
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION                      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   CREW ORCHESTRATOR                      │
│  - Manages agent handoffs                               │
│  - Handles task delegation                              │
│  - Aggregates results                                   │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   AGENT 1    │ │   AGENT 2    │ │   AGENT 3    │
│  Researcher  │ │   Analyst    │ │    Writer    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│    TOOLS     │ │    TOOLS     │ │    TOOLS     │
│ - Web Search │ │ - Calculator │ │ - Formatter  │
│ - Scraper    │ │ - Summarizer │ │ - Templates  │
└──────────────┘ └──────────────┘ └──────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 OLLAMA (LOCAL LLM)                       │
│  - llama3.2 / mistral / codellama                       │
│  - Runs on YOUR machine                                 │
│  - No API costs, no rate limits                         │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
autogen-business-agents/
├── agents/                 # Agent definitions
│   ├── __init__.py
│   ├── meeting_prep.py     # Meeting preparation crew
│   ├── lead_research.py    # Lead/company research crew
│   └── base.py             # Base agent configuration
├── tools/                  # Custom tools for agents
│   ├── __init__.py
│   ├── search.py           # Web search tools
│   └── formatters.py       # Output formatting
├── configs/                # Configuration files
│   └── models.py           # LLM configuration
├── examples/               # Ready-to-run examples
│   └── meeting_prep_example.py
├── docs/                   # Documentation
│   └── ARCHITECTURE.md
├── requirements.txt
├── .env.example
└── README.md
```

---

## Configuration

### Using Ollama (Default - Free)

No configuration needed. Just ensure Ollama is running:

```bash
ollama serve
```

### Using OpenAI (Optional)

If you prefer OpenAI, create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

---

## Extending

### Adding a New Agent

1. Create a new file in `agents/`
2. Define your agents and their roles
3. Create a Crew that orchestrates them
4. Add an example in `examples/`

See `agents/meeting_prep.py` for a complete example.

### Adding Custom Tools

Tools give agents capabilities beyond text generation:

```python
from crewai.tools import tool

@tool("Company Lookup")
def lookup_company(company_name: str) -> str:
    """Looks up company information from public sources."""
    # Your implementation here
    return company_info
```

---

## Roadmap

- [x] Meeting Prep Agent
- [ ] Lead Research Agent
- [ ] Document Q&A Agent (RAG)
- [ ] Email Drafter Agent
- [ ] Competitive Intel Agent
- [ ] Slack Integration
- [ ] API wrapper for all agents

---

## Why CrewAI?

I evaluated AutoGen, LangGraph, and CrewAI. Here's why I chose CrewAI for this project:

| Framework | Pros | Cons |
|-----------|------|------|
| **CrewAI** | Simple API, great docs, fast to ship | Less flexible than LangGraph |
| AutoGen | Microsoft backing, enterprise feel | Steeper learning curve |
| LangGraph | Most flexible, fine-grained control | Complex for simple use cases |

For business automation agents, **simplicity wins**. These agents need to be maintainable by teams, not just AI engineers.

---

## Contributing

PRs welcome. Please:

1. Keep agents focused on real business use cases
2. Include working examples
3. Test with Ollama (free tier must work)

---

## License

MIT - Use it however you want.

---

## About

Built by [Chris Damien](https://linkedin.com/in/chris-damien) as part of my work helping businesses automate with AI.

**More resources:**
- [LinkedIn](https://linkedin.com/in/chris-damien) - I write about AI automation weekly
- [Other Projects](https://github.com/chris-damien) - More automation tools

---

*If this helped you, star the repo ⭐*
