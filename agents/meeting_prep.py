"""
Meeting Prep Agent
------------------
A multi-agent crew that prepares you for meetings by:
1. Researching attendees
2. Analyzing company/context
3. Drafting agenda and talking points

Usage:
    from agents.meeting_prep import prepare_for_meeting
    
    result = prepare_for_meeting(
        meeting_title="Q1 Partnership Discussion",
        attendees=["John Smith - Acme Corp CEO", "Jane Doe - Acme Corp CTO"],
        context="Initial partnership exploration meeting"
    )
"""

from crewai import Agent, Task, Crew, Process
from configs.models import get_llm
from tools.search import web_search, linkedin_search, company_search
from tools.formatters import format_meeting_agenda, format_briefing


def create_meeting_prep_crew(verbose: bool = True):
    """
    Creates a crew of agents specialized in meeting preparation.
    
    Returns:
        Tuple of (agents, crew)
    """
    llm = get_llm()
    
    # ===========================================
    # AGENT 1: Research Analyst
    # ===========================================
    researcher = Agent(
        role="Research Analyst",
        goal="Gather comprehensive background information on meeting attendees and their companies",
        backstory="""You are an expert research analyst who specializes in 
        preparing executives for important meetings. You dig deep to find 
        relevant professional backgrounds, company news, and potential 
        talking points. You focus on actionable intelligence, not fluff.""",
        tools=[web_search, linkedin_search, company_search],
        llm=llm,
        verbose=verbose,
    )
    
    # ===========================================
    # AGENT 2: Strategic Advisor
    # ===========================================
    strategist = Agent(
        role="Strategic Advisor", 
        goal="Analyze research and identify key opportunities, risks, and recommended talking points",
        backstory="""You are a seasoned business strategist who helps executives 
        prepare for high-stakes meetings. You excel at connecting dots between 
        research findings and strategic opportunities. You think about what 
        questions to ask, what topics to avoid, and how to build rapport.""",
        tools=[],
        llm=llm,
        verbose=verbose,
    )
    
    # ===========================================
    # AGENT 3: Meeting Planner
    # ===========================================
    planner = Agent(
        role="Meeting Planner",
        goal="Create a structured, actionable meeting prep document with agenda and briefing",
        backstory="""You are an expert at distilling complex information into 
        clear, actionable meeting prep documents. You create agendas that 
        keep meetings on track and briefings that executives can scan in 
        5 minutes. You focus on what matters most.""",
        tools=[format_meeting_agenda, format_briefing],
        llm=llm,
        verbose=verbose,
    )
    
    return {
        "researcher": researcher,
        "strategist": strategist,
        "planner": planner,
    }


def prepare_for_meeting(
    meeting_title: str,
    attendees: list[str],
    context: str = "",
    your_goals: str = "",
    verbose: bool = True,
) -> str:
    """
    Prepare comprehensive materials for an upcoming meeting.
    
    Args:
        meeting_title: Title/purpose of the meeting
        attendees: List of attendees (format: "Name - Title at Company")
        context: Additional context about the meeting
        your_goals: What you want to achieve in this meeting
        verbose: Whether to show agent reasoning
        
    Returns:
        Complete meeting prep document
    """
    agents = create_meeting_prep_crew(verbose=verbose)
    
    attendee_str = "\n".join(f"- {a}" for a in attendees)
    
    # ===========================================
    # TASK 1: Research Attendees
    # ===========================================
    research_task = Task(
        description=f"""Research the following meeting attendees thoroughly:

{attendee_str}

For each person, find:
1. Professional background and current role
2. Recent news or accomplishments
3. Their company's recent developments
4. Any mutual connections or shared interests
5. Communication style hints (if available)

Meeting context: {context}
""",
        expected_output="""A detailed research brief on each attendee including:
- Professional background summary
- Recent news/accomplishments
- Company context
- Potential conversation starters""",
        agent=agents["researcher"],
    )
    
    # ===========================================
    # TASK 2: Strategic Analysis
    # ===========================================
    strategy_task = Task(
        description=f"""Based on the research provided, develop a strategic approach for this meeting.

Meeting: {meeting_title}
Context: {context}
Goals: {your_goals if your_goals else "General relationship building and exploration"}

Analyze:
1. What are the key opportunities in this meeting?
2. What topics should we emphasize?
3. What topics should we be careful about or avoid?
4. What questions should we ask?
5. How can we build rapport with each attendee?
6. What objections might come up and how to handle them?
""",
        expected_output="""Strategic recommendations including:
- Key opportunities identified
- Recommended talking points (prioritized)
- Topics to avoid or handle carefully  
- Questions to ask
- Rapport-building suggestions
- Objection handling strategies""",
        agent=agents["strategist"],
    )
    
    # ===========================================
    # TASK 3: Create Prep Document
    # ===========================================
    prep_task = Task(
        description=f"""Create a complete meeting preparation document that includes:

1. EXECUTIVE SUMMARY (2-3 sentences max)
2. ATTENDEE PROFILES (key facts only, scannable)
3. STRATEGIC APPROACH (from strategist's analysis)
4. SUGGESTED AGENDA (with time allocations)
5. TALKING POINTS (prioritized, with supporting context)
6. QUESTIONS TO ASK (prioritized)
7. THINGS TO AVOID
8. SUCCESS CRITERIA (how we'll know the meeting went well)

Meeting details:
- Title: {meeting_title}
- Attendees: {attendee_str}
- Context: {context}
- Goals: {your_goals if your_goals else "Relationship building and exploration"}

Format this so an executive can scan it in 5 minutes and feel prepared.
""",
        expected_output="""A complete, well-formatted meeting prep document that is:
- Scannable in 5 minutes
- Actionable with clear talking points
- Strategic with clear goals
- Professional in formatting""",
        agent=agents["planner"],
    )
    
    # ===========================================
    # CREATE AND RUN CREW
    # ===========================================
    crew = Crew(
        agents=list(agents.values()),
        tasks=[research_task, strategy_task, prep_task],
        process=Process.sequential,
        verbose=verbose,
    )
    
    result = crew.kickoff()
    
    return result


# ===========================================
# CLI INTERFACE
# ===========================================
if __name__ == "__main__":
    # Example usage
    result = prepare_for_meeting(
        meeting_title="Q1 Partnership Discussion",
        attendees=[
            "Satya Nadella - CEO at Microsoft",
            "Kevin Scott - CTO at Microsoft",
        ],
        context="Initial exploration of potential AI partnership",
        your_goals="Understand their AI strategy and identify collaboration opportunities",
    )
    
    print("\n" + "="*60)
    print("MEETING PREP COMPLETE")
    print("="*60)
    print(result)
