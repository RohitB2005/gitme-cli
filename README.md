# gitme-cli

AI-powered git commit message generator. Reads your staged changes and generates a well-formatted [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) message using a local or cloud LLM.

**Local-first and privacy-friendly by default** — your diffs never leave your machine unless you choose a cloud provider.

---

## Requirements

- Python 3.11 or higher
- Git

---

## Installation

```bash
pip install gitme-cli
```

---

## Quick Start

Stage your changes as you normally would, then run `gitme`:

```bash
git add .
gitme
```

That's it. gitme reads your staged diff, sends it to the AI, and prints a suggested commit message in your terminal.

By default it uses **Ollama with llama3.2** running locally. See [Providers](#providers) below to set up Ollama or switch to a cloud provider.

---

## Usage

### Basic

```bash
gitme
```

### Copy to clipboard

```bash
gitme --copy
```

The message is printed to the terminal and copied to your clipboard. You can then paste it directly into `git commit -m "..."`.

### Add extra context

```bash
gitme --context "this is a hotfix for the login bug in production"
```

The context is appended to the prompt so the model has more information to work with. Useful when the diff alone doesn't tell the full story.

---

## Providers

gitme supports three providers. You set your preferred one once and it applies to every future run.

### Ollama (default — local, free, private)

Ollama runs models on your own machine. No API key needed, no data leaves your computer.

**1. Install Ollama**

Download from [ollama.com](https://ollama.com) and open the app. You'll see it in your menu bar when it's running.

**2. Pull the model**

```bash
ollama pull llama3.2
```

**3. Run gitme**

```bash
gitme
```

Ollama is already the default — nothing else to configure.

To use a different Ollama model:

```bash
gitme-config set model mistral
```

---

### OpenAI (cloud, best quality)

Uses the OpenAI API. You need an API key and credit — `gpt-4o-mini` is cheap and works well for commit messages.

**1. Set your API key**

```bash
gitme-config set openai_api_key YOUR_API_KEY
gitme-config set provider openai
gitme-config set model gpt-4o-mini
```

**2. Run gitme**

```bash
gitme
```

Your API key is stored locally in `~/.gitme.toml` and never shared.

---

### OpenRouter (cloud, free tier available)

OpenRouter provides access to many models including free ones. No credit card required for the free tier.

Get a free API key at [openrouter.ai](https://openrouter.ai).

**1. Set your API key**

```bash
gitme-config set openrouter_api_key YOUR_API_KEY
gitme-config set provider openrouter
gitme-config set model "nvidia/nemotron-3-nano-30b-a3b:free"
```

**2. Run gitme**

```bash
gitme
```

---

## Configuration

Configuration is stored in `~/.gitme.toml` and shared across all your projects.

### View current config

```bash
gitme-config show
```

Output:
```
provider: ollama
model: llama3.2
style: conventional
```

### Set a value

```bash
gitme-config set <key> <value>
```

**Available keys:**

| Key | Description | Default |
|-----|-------------|---------|
| `provider` | Which provider to use: `ollama`, `openai`, or `openrouter` | `ollama` |
| `model` | Model name for the active provider | `llama3.2` |
| `style` | Commit style (currently `conventional`) | `conventional` |
| `openai_api_key` | Your OpenAI API key | — |
| `openrouter_api_key` | Your OpenRouter API key | — |

### Examples

```bash
# Switch to OpenAI
gitme-config set provider openai
gitme-config set model gpt-4o-mini
gitme-config set openai_api_key sk-...

# Switch back to Ollama
gitme-config set provider ollama
gitme-config set model llama3.2
```

---

## Commit Format

gitme follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) specification:

```
type(scope): short description

- optional body explaining why the change was made

Fixes #123  (optional footer)
```

**Commit types:**

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructured without changing behaviour |
| `docs` | Documentation changes only |
| `style` | Formatting or whitespace, no logic changes |
| `test` | Adding or updating tests |
| `chore` | Maintenance, config changes, dependency updates |

---

## License

MIT