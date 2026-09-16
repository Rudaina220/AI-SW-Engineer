from tools.groq_client import ask_llm


class PlanningAgent:

    def create_plan(
        self,
        task: str,
        analysis: str
    ):

        prompt = f"""
You are a senior software engineer.

USER TASK:

{task}

CODEBASE ANALYSIS:

{analysis}

Create a step-by-step implementation plan.

For each step provide:

- File to modify
- What to change
- Why it is needed

Do not write code yet.
"""

        return ask_llm(prompt)