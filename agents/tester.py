from tools.terminal import run_command


class TestAgent:

    def run_tests(
        self,
        repo_path: str
    ):

        result = run_command(
            "python -m pytest",
            repo_path
        )

        return result