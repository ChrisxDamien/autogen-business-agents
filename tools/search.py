"""
Search Tools
------------
Web search capabilities for agents using DuckDuckGo (free, no API key).
"""

from crewai.tools import tool
from duckduckgo_search import DDGS


@tool("Web Search")
def web_search(query: str) -> str:
    """
    Search the web for information. Use this to find current information
    about people, companies, news, or any topic.
    
    Args:
        query: The search query string
        
    Returns:
        Search results as formatted text
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return f"No results found for: {query}"
        
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r['title']}\n   {r['body']}\n   Source: {r['href']}")
        
        return "\n\n".join(formatted)
    
    except Exception as e:
        return f"Search error: {str(e)}"


@tool("LinkedIn Search")
def linkedin_search(person_name: str, company: str = "") -> str:
    """
    Search for professional information about a person.
    
    Args:
        person_name: Name of the person to research
        company: Optional company name to narrow results
        
    Returns:
        Professional information found
    """
    query = f"{person_name} {company} LinkedIn profile background"
    return web_search(query)


@tool("Company Search")
def company_search(company_name: str) -> str:
    """
    Search for information about a company.
    
    Args:
        company_name: Name of the company to research
        
    Returns:
        Company information found
    """
    query = f"{company_name} company overview business"
    return web_search(query)
