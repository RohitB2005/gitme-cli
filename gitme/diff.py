import subprocess

def get_staged_diff() -> str:
    repo_exists = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True
    )

    if repo_exists.returncode != 0:
        raise EnvironmentError("Not currently inside a git repository.")
    
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Git error: {result.stderr.strip()}")
    
    diff = result.stdout.strip()

    if not diff:
        raise ValueError("No staged changes found. Run 'git add' first.")
    
    return diff