from pathlib import Path


def get_file_tree(repo_path: str) -> str:
    repo = Path(repo_path)

    files = []

    for path in repo.rglob("*"):

        if ".git" in path.parts:
            continue

        if "__pycache__" in path.parts:
            continue

        if path.is_file():
            files.append(
                str(path.relative_to(repo))
            )

    return "\n".join(files)


def read_file(repo_path: str, file_path: str) -> str:
    path = Path(repo_path) / file_path

    return path.read_text(
        encoding="utf-8"
    )


def write_file(
    repo_path: str,
    file_path: str,
    content: str
):
    repo = Path(repo_path).resolve()

    # Remove accidental markdown/code formatting
    file_path = file_path.strip()
    file_path = file_path.replace("```", "")

    # If the LLM accidentally returns the repository path,
    # keep only the part after it.
    repo_str = str(repo)

    if file_path.startswith(repo_str):
        file_path = file_path[len(repo_str):].lstrip("\\/")

    # Handle paths such as:
    # "Repository path: workspace/test_fastapi/app/main.py"
    if "Repository path:" in file_path:
        file_path = file_path.split("Repository path:", 1)[1].strip()

    # Normalize Windows separators
    file_path = file_path.replace("\\", "/")

    path = repo / file_path

    # Security check: don't allow the LLM to write outside repo
    try:
        path.resolve().relative_to(repo)
    except ValueError:
        raise ValueError(
            f"Invalid file path outside repository: {file_path}"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        content,
        encoding="utf-8"
    )