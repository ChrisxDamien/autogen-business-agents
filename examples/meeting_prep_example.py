#!/usr/bin/env python3
"""
Meeting Prep Example
--------------------
Run this to see the Meeting Prep Agent in action.

Prerequisites:
1. Install dependencies: pip install -r requirements.txt
2. Start Ollama: ollama serve
3. Pull a model: ollama pull llama3.2

Usage:
    python examples/meeting_prep_example.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from agents.meeting_prep import prepare_for_meeting

console = Console()


def main():
    console.print(Panel.fit(
        "[bold blue]🤖 Meeting Prep Agent Demo[/bold blue]\n"
        "Preparing briefing materials for your meeting...",
        border_style="blue"
    ))
    
    # =========================================
    # CUSTOMIZE YOUR MEETING HERE
    # =========================================
    
    meeting_title = "Partnership Exploration Call"
    
    attendees = [
        "Tim Cook - CEO at Apple",
        "Craig Federighi - SVP Software Engineering at Apple",
    ]
    
    context = """
    This is an initial call to explore potential partnership opportunities
    in the AI automation space. We want to understand their needs and see
    if there's alignment with our capabilities.
    """
    
    your_goals = """
    1. Understand their current AI automation challenges
    2. Identify potential areas for collaboration
    3. Establish a follow-up meeting with technical teams
    """
    
    # =========================================
    # RUN THE AGENT CREW
    # =========================================
    
    console.print("\n[yellow]Starting research and analysis...[/yellow]\n")
    console.print("[dim]This may take 1-2 minutes depending on your model.[/dim]\n")
    
    try:
        result = prepare_for_meeting(
            meeting_title=meeting_title,
            attendees=attendees,
            context=context,
            your_goals=your_goals,
            verbose=True,  # Set to False to hide agent reasoning
        )
        
        console.print("\n")
        console.print(Panel(
            str(result),
            title="[bold green]✅ Meeting Prep Complete[/bold green]",
            border_style="green",
            padding=(1, 2),
        ))
        
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        console.print("\n[yellow]Troubleshooting tips:[/yellow]")
        console.print("1. Is Ollama running? Try: ollama serve")
        console.print("2. Do you have a model? Try: ollama pull llama3.2")
        console.print("3. Check your .env configuration")
        raise


if __name__ == "__main__":
    main()
