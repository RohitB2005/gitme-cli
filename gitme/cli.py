import click
from rich.console import Console
from rich.panel import Panel

from .diff import get_staged_diff
from .prompt import SYSTEM_PROMPT, build_prompt
from .providers.ollama import OllamaProvider
from .providers.openai import OpenAIProvider
from .providers.openrouter import OpenRouterProvider
from .config import load_config, save_config, show_config

console = Console()


def get_provider(cfg: dict):
    provider = cfg.get("provider", "ollama")
    model = cfg.get("model", "llama3.2")

    if provider == "ollama":
        return OllamaProvider(model=model)
    elif provider == "openai":
        return OpenAIProvider(model=model, api_key=cfg.get("openai_api_key", ""))
    elif provider == "openrouter":
        return OpenRouterProvider(model=model, api_key=cfg.get("openrouter_api_key", ""))
    else:
        raise RuntimeError(
            f"Unknown provider '{provider}'. Choose: ollama, openai, openrouter"
        )


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
        cfg = load_config()
        provider = get_provider(cfg)
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


@click.group()
def config():
    """Manage gitme configuration."""
    pass


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a config value. E.g: gitme-config set provider openai"""
    valid_keys = ["provider", "model", "style", "openai_api_key", "openrouter_api_key"]
    if key not in valid_keys:
        console.print(f"[red]Unknown key '{key}'. Valid keys: {', '.join(valid_keys)}[/red]")
        raise SystemExit(1)
    save_config({key: value})
    console.print(f"[green]Set {key} = {value}[/green]")


@config.command("show")
def config_show():
    """Show current configuration."""
    cfg = show_config()
    for key, value in cfg.items():
        console.print(f"[dim]{key}:[/dim] {value}", highlight=False)