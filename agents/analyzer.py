from tools.filesystem import (
    get_file_tree,
    read_file
)

from tools.groq_client import ask_llm


class CodebaseAnalyzer:

    def analyze(
        self,
        repo_path: str,
        task: str
    ):

        tree = get_file_tree(repo_path)

        important_files = []

        for file in tree.split("\n"):

            if (
                file.endswith(".py")
                or file.endswith(".txt")
                or file.endswith(".json")
            ):
                important_files.append(file)

        files_content = ""

        for file in important_files[:10]:

            try:

                content = read_file(
                    repo_path,
                    file
                )

                files_content += f"""

FILE: {file}

{content}

-------------------
"""

            except Exception:
                pass

        prompt = f"""
You are analyzing a software repository.

USER TASK:

{task}

ACTUAL FILE TREE:

{tree}

ACTUAL FILE CONTENT:

{files_content}

IMPORTANT:

Only refer to files that actually appear in the ACTUAL FILE TREE.

Do NOT invent files, folders, technologies, endpoints,
routers, models, databases, or architecture.

If something is unknown, explicitly say:
"Not present in the repository."

Explain:

1. Technologies actually detected
2. How the application currently works
3. Important existing files
4. Where the requested change should be made
5. Potential risks

Keep the answer structured and concise.
"""

        return ask_llm(prompt)