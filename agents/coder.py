import json

from tools.filesystem import (
    get_file_tree,
    read_file,
    write_file
)

from tools.groq_client import ask_llm


class CodingAgent:

    def implement(
        self,
        repo_path: str,
        task: str,
        plan: str
    ):

        tree = get_file_tree(repo_path)

        code_context = ""

        for file in tree.split("\n"):

            if file.endswith(".py"):

                try:

                    content = read_file(
                        repo_path,
                        file
                    )

                    code_context += f"""

FILE: {file}

{content}

----------------
"""

                except Exception:
                    pass

        prompt = f"""
You are an AI coding agent.

TASK:

{task}

PLAN:

{plan}

CURRENT CODE:

{code_context}

Modify the repository to complete the task.

IMPORTANT FILE PATH RULES:

- The "path" field MUST be relative to the repository root.
- NEVER include the repository path.
- NEVER include "Repository path:".
- NEVER use an absolute Windows path.
- NEVER use "workspace/" at the beginning.
- Examples of valid paths:
  "main.py"
  "app/data.py"
  "app/models.py"
  "tests/test_users.py"

Return ONLY valid JSON.

Format:

{{
    "files": [
        {{
            "path": "app/data.py",
            "content": "COMPLETE FILE CONTENT"
        }}
    ]
}}

Only include files that need to be created or modified.
"""

        response = ask_llm(prompt)

        response = response.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )

        data = json.loads(response)

        changed_files = []

        for file in data["files"]:

            write_file(
                repo_path,
                file["path"],
                file["content"]
            )

            changed_files.append(
                file["path"]
            )

        return changed_files