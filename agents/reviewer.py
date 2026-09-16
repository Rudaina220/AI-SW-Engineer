from tools.terminal import run_command
from tools.groq_client import ask_llm


class CodeReviewAgent:

    def review(
        self,
        repo_path: str
    ):

        diff = run_command(
            "git diff",
            repo_path
        )

        prompt = f"""
You are performing a code review.

Review this git diff:

{diff["output"]}

Check for:

- Bugs
- Security issues
- Bad practices
- Missing error handling
- Unnecessary complexity

Return a concise review.
"""

        return ask_llm(prompt)