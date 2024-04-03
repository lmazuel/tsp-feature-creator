from github.Issue import Issue
from gh_token import GITHUB_TOKEN


from github import Auth, Github


def get_repo(repo_name):
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    return repo


def create_issue(repo_name, title):
    repo = get_repo(repo_name)
    try:
        return repo.create_issue(title=title)
    except Exception as e:
        print(f"Error creating issue: {e}")
        print(f"Repo: {repo_name}")
        raise


def create_task_list(issues: list[Issue], task_type: str) -> str:
    """
    Creates a task list with the given issues and task type.

    Args:
        issues (list[Issue]): A list of issues.
        task_type (str): The type of task.

    Returns:
        str: The task list as a string.
    """
    buffer = f"```[tasklist]\n### {task_type}\n"
    for issue in issues:
        buffer += f"- [ ] {issue.html_url}\n"
    buffer += "```"
    return buffer