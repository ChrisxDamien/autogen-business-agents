"""
Formatter Tools
---------------
Output formatting utilities for agents.
"""

from crewai.tools import tool
from datetime import datetime


@tool("Format Meeting Agenda")
def format_meeting_agenda(
    title: str,
    attendees: str,
    topics: str,
    duration_minutes: int = 30
) -> str:
    """
    Format a meeting agenda in a professional structure.
    
    Args:
        title: Meeting title
        attendees: Comma-separated list of attendees
        topics: Comma-separated list of discussion topics
        duration_minutes: Expected meeting duration
        
    Returns:
        Formatted meeting agenda
    """
    attendee_list = [a.strip() for a in attendees.split(",")]
    topic_list = [t.strip() for t in topics.split(",")]
    
    agenda = f"""
═══════════════════════════════════════════════════════
MEETING AGENDA: {title}
═══════════════════════════════════════════════════════

📅 Date: [To be scheduled]
⏱️  Duration: {duration_minutes} minutes

👥 ATTENDEES:
{chr(10).join(f"   • {a}" for a in attendee_list)}

📋 AGENDA:
{chr(10).join(f"   {i+1}. {t}" for i, t in enumerate(topic_list))}

📝 NOTES:
   [Space for meeting notes]

═══════════════════════════════════════════════════════
"""
    return agenda.strip()


@tool("Format Briefing Document")
def format_briefing(
    subject: str,
    key_points: str,
    background: str,
    recommendations: str = ""
) -> str:
    """
    Format a briefing document for pre-meeting preparation.
    
    Args:
        subject: Subject of the briefing
        key_points: Main points (comma-separated)
        background: Background context
        recommendations: Optional recommendations
        
    Returns:
        Formatted briefing document
    """
    points = [p.strip() for p in key_points.split(",")]
    
    doc = f"""
┌─────────────────────────────────────────────────────┐
│  BRIEFING: {subject}
│  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
└─────────────────────────────────────────────────────┘

KEY POINTS:
{chr(10).join(f"  ★ {p}" for p in points)}

BACKGROUND:
{background}
"""
    
    if recommendations:
        doc += f"""
RECOMMENDATIONS:
{recommendations}
"""
    
    return doc.strip()
