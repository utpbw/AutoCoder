import yaml
from hstest import StageTest, CheckResult, dynamic_test
from github import Github, GithubException
from AutoCoder.task.main import url

import os


class GitTest(StageTest):
    g = Github(os.getenv("GITHUB_TOKEN")) if os.getenv("GITHUB_TOKEN") else Github()

    repo_name = url.split('/')[-1].replace('.git', '')
    username = url.split('/')[-2]
    full_repo_name = f"{username}/{repo_name}"
    repo = g.get_repo(full_repo_name)

    @dynamic_test()
    def check_repo(self):
        try:
            if self.repo.private:
                return CheckResult.wrong("The repository is private. Make sure it's public.")
            return CheckResult.correct()
        except GithubException as e:
            if e.status == 404:
                return CheckResult.wrong("The repository does not exist or cannot be accessed.")
            else:
                return CheckResult.wrong(
                    f"An error occurred while accessing the GitHub repository: {e.data.get('message', 'No error message')}")
        except Exception as e:
            return CheckResult.wrong(f"Something went wrong. Encountered: {e}")

    @dynamic_test
    def check_issues_exist(self):
        try:
            issues = list(self.repo.get_issues(state="open"))
            if not issues:
                return CheckResult.wrong("No open issues found in the repository.")
            return CheckResult.correct()
        except GithubException as e:
            return CheckResult.wrong(f"An error occurred while accessing the repository: {e.data.get('message', 'No error message')}")
        except Exception as e:
            return CheckResult.wrong(f"An unexpected error occurred: {e}")

    @dynamic_test
    def check_issue_properties(self):
        try:
            issues = list(self.repo.get_issues(state="open"))
            autocoder_issues = [issue for issue in issues if "autocoder-bot" in [label.name for label in issue.labels] and issue.pull_request is None]

            if not autocoder_issues:
                return CheckResult.wrong("No issues with the 'autocoder-bot' label found.")

            for issue in autocoder_issues:
                if not issue.body:
                    return CheckResult.wrong(f"The issue #{issue.number} does not have any content.")
                if len(issue.body.split()) < 50:
                    return CheckResult.wrong(f"The issue #{issue.number} is too short. Make sure it is at least 50 words.")
            return CheckResult.correct()
        except GithubException as e:
            return CheckResult.wrong(f"An error occurred while accessing the repository: {e.data.get('message', 'No error message')}")
        except Exception as e:
            return CheckResult.wrong(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    GitTest().run_tests()