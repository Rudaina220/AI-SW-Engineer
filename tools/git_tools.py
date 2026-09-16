import subprocess


def run_git_command(command, repo_path):
    result = subprocess.run(
        command,
        cwd=repo_path,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "return_code": result.returncode,
        "output": result.stdout + result.stderr
    }


def git_status(repo_path):
    return run_git_command("git status --short", repo_path)


def git_commit(repo_path, message):
    add_result = run_git_command("git add .", repo_path)

    if add_result["return_code"] != 0:
        return add_result

    return run_git_command(
        f'git commit -m "{message}"',
        repo_path
    )


def git_push(repo_path):
    return run_git_command("git push origin main", repo_path)