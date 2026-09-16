from tools.filesystem import (
    get_file_tree,
    read_file,
    write_file
)

from tools.groq_client import ask_llm

import json


class DebugAgent:

    def fix(
        self,
        repo_path: str,
        task: str,
        error: str
    ):

        tree = get_file_tree(repo_path)

        context = ""

        for file in tree.split("\n"):

            if file.endswith(".py"):

                try:

                    content = read_file(
                        repo_path,
                        file
                    )

                    context += f"""

FILE: {file}

{content}

----------------
"""

                except Exception:
                    pass

        prompt = f"""
You are debugging a Python application.

TASK:

{task}

TEST ERROR:

{error}

CURRENT CODE:

{context}

Fix the problem.

Return ONLY valid JSON:

{{
    "files": [
        {{
            "path": "file.py",
            "content": "complete corrected content"
        }}
    ]
}}
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

        fixed_files = []

        for file in data["files"]:

            write_file(
                repo_path,
                file["path"],
                file["content"]
            )

            fixed_files.append(
                file["path"]
            )

        return fixed_files