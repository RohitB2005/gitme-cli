import click
from rich.console import Console
from rich.panel import Panel

from .diff import get_staged_diff
from .prompt import SYSTEM_PROMPT, build_prompt
from .providers.ollama import OllamaProvider

console = Console()

@click.command()
@click.option("--copy", is_flag=True, help="Copy the result to clipboard.")
@click.option("--context", default="", help="Extra context to include in the prompt.")
def main(copy, context):
    """Generate a git commit message from your staged changes."""
    try:
        diff = get_staged_diff()
    except (EnvironmentError, ValueError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)
    
    user_prompt = build_prompt(diff)
    if context:
        user_prompt += f"\n\nExtra context: {context}"
    console.print("[dim]Generating commit message...[/dim]")

    try: 
        provider = OllamaProvider()
        message = provider.generate(SYSTEM_PROMPT, user_prompt)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)
    
    console.print(Panel(message, title="suggested commit message", border_style="green"))

    if copy:
        try:
            import pyperclip
            pyperclip.copy(message)
            console.print("[dim]Copied to clipboard.[/dim]")
        except Exception:
            console.print("[yellow]Could not copy to clipboard.[/yellow]")