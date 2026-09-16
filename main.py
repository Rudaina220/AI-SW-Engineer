from agents.analyzer import CodebaseAnalyzer
from agents.planner import PlanningAgent
from agents.coder import CodingAgent
from agents.tester import TestAgent
from agents.debugger import DebugAgent
from agents.reviewer import CodeReviewAgent

from tools.git_tools import git_status, git_commit, git_push

from config import MAX_DEBUG_ATTEMPTS


def run_agent(
    repo_path: str,
    task: str
):

    print("\n" + "=" * 60)
    print("AI SOFTWARE ENGINEER AGENT")
    print("=" * 60)

    analyzer = CodebaseAnalyzer()
    planner = PlanningAgent()
    coder = CodingAgent()
    tester = TestAgent()
    debugger = DebugAgent()
    reviewer = CodeReviewAgent()

    print("\n[1] ANALYZING CODEBASE...")

    analysis = analyzer.analyze(
        repo_path,
        task
    )

    print(analysis)

    print("\n[2] CREATING PLAN...")

    plan = planner.create_plan(
        task,
        analysis
    )

    print(plan)

    print("\n[3] IMPLEMENTING...")

    changed_files = coder.implement(
        repo_path,
        task,
        plan
    )

    print("Changed files:")

    for file in changed_files:
        print("-", file)

    print("\n[4] RUNNING TESTS...")

    test_result = tester.run_tests(
        repo_path
    )

    attempts = 0

    while (
        test_result["return_code"] != 0
        and attempts < MAX_DEBUG_ATTEMPTS
    ):

        attempts += 1

        print(
            f"\n[DEBUG ATTEMPT {attempts}]"
        )

        print(test_result["output"])

        debugger.fix(
            repo_path,
            task,
            test_result["output"]
        )

        print("\nRUNNING TESTS AGAIN...")

        test_result = tester.run_tests(
            repo_path
        )

    if test_result["return_code"] == 0:

        print("\nTESTS PASSED")

    else:

        print("\nTESTS STILL FAILING")

        print(test_result["output"])

        return

    print("\n[5] CODE REVIEW...")

    review = reviewer.review(
        repo_path
    )

    print(review)

    print("\n[6] GIT STATUS")

    print(
        git_status(repo_path)["output"]
    )

    commit = git_commit(repo_path, "feat: implement requested feature")
    print(commit["output"])

    if commit["return_code"] == 0:
        print("\n[7] PUSHING TO GITHUB...")
        push = git_push(repo_path)
        print(push["output"])

        if push["return_code"] != 0:
            print("\nGITHUB PUSH FAILED")
            return

    print("\nDONE.")


if __name__ == "__main__":

    repo_path = input(
        "Repository path: "
    )

    task = input(
        "What should the agent do? "
    )

    run_agent(
        repo_path,
        task
    )