import subprocess


def run_command(
    command: str,
    cwd: str
):
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True
    )

    output = (
        result.stdout
        + "\n"
        + result.stderr
    )

    return {
        "return_code": result.returncode,
        "output": output
    }