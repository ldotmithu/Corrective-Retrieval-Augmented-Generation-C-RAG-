import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from src.helper import *
from src.State import AgentState
from src.Workflow import BuildGraph

console = Console()

def main():
    console.print(
        Panel.fit(
            "[bold green]🚀 Corrective RAG Agent[/bold green]\n"
            "Type your question and press [cyan]Enter[/cyan].\n"
            "Type [red]'exit'[/red] to quit.",
            border_style="green",
        )
    )

    # Build workflow
    workflow = BuildGraph()
    compiled_graph = workflow.build_graph()

    while True:
        # User input
        user_question = Prompt.ask("[bold cyan]You[/bold cyan]")
        if user_question.lower() in ["exit", "quit", "q"]:
            console.print("\n[bold red]👋 Exiting... Bye![/bold red]")
            sys.exit(0)

        try:
            # Run through workflow
            shared_state = compiled_graph.invoke({"question": user_question})

            # Agent response
            agent_response = shared_state.get("agent_response", "⚠️ No response generated.")
            console.print(
                Panel(agent_response, title="[bold magenta]Agent[/bold magenta]", border_style="magenta")
            )
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
