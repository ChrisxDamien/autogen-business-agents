"""
LLM Configuration
-----------------
Handles switching between Ollama (free), OpenAI, Groq, etc.
"""

import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def get_llm():
    """
    Returns the configured LLM based on environment variables.
    Defaults to Ollama (free, local) if no provider specified.
    """
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        return ChatOllama(
            model=model,
            temperature=0.7,
        )
    
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    
    elif provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY"),
        )
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


# Default LLM instance
llm = get_llm()
