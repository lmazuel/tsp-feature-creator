from typing import Optional
from github.Issue import Issue
from gh_token import GITHUB_TOKEN
from gql_tools import GithubGqlClient


from github import Auth, Github


def get_repo(repo_name):
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    return repo


_gh_gql_client = None


def get_gql_client():
    global _gh_gql_client
    if _gh_gql_client is None:
        _gh_gql_client = GithubGqlClient(GITHUB_TOKEN)
    return _gh_gql_client


def create_issue(
    repo_name: str,
    title: str,
    *,
    project_id: str | None = None,
    labels: list[str] | None = None,
) -> Issue:
    if not labels:
        labels = []
    repo = get_repo(repo_name)
    try:
        issue = repo.create_issue(title=title, labels=labels)

        if project_id:
            add_to_project(project_id, issue)
        return issue
    except Exception as e:
        print(f"Error creating issue: {e}")
        print(f"Repo: {repo_name}")
        raise


def get_issue(repo_name: str, issue_number: int) -> Issue:
    """
    Retrieves an issue from a given repository.

    Args:
        repo_name (str): The name of the repository.
        issue_number (int): The number of the issue.

    Returns:
        Issue: The retrieved issue object.
    """
    repo = get_repo(repo_name)
    issue = repo.get_issue(issue_number)
    return issue


def add_to_project(project_id: str, issue: Issue) -> None:
    node_id = get_node_id(issue)
    client = get_gql_client()
    client.add_issue_to_project(project_id, node_id)


def get_node_id(issue: Issue) -> str:
    """
    Get the node ID of an issue.

    Parameters:
    issue (object): The issue object.

    Returns:
    str: The node ID of the issue.
    """
    return issue.raw_data["node_id"]


def create_task_list(issues: list[Optional[Issue]], task_type: str) -> str:
    """
    Creates a task list with the given issues and task type.

    Args:
        issues (list[Issue]): A list of issues. Can be None.
        task_type (str): The type of task.

    Returns:
        str: The task list as a string.
    """
    buffer = f"### {task_type}\n"
    for issue in issues:
        if not issue:
            continue
        buffer += f"- [ ] {issue.html_url}\n"
    return buffer


def add_sub_issue(parent_issue: Issue, sub_issue: Issue) -> None:
    """
    Adds a sub-issue relationship between two issues.

    Args:
        parent_issue (Issue): The parent issue.
        sub_issue (Issue): The sub-issue to be added as a child.
    """
    parent_node_id = get_node_id(parent_issue)
    sub_issue_node_id = get_node_id(sub_issue)
    client = get_gql_client()
    try:
        client.add_sub_issue(parent_node_id, sub_issue_node_id)
        print(f"Successfully added sub-issue relationship: {sub_issue.html_url} -> {parent_issue.html_url}")
    except Exception as e:
        print(f"Error adding sub-issue relationship: {e}")
        raise
