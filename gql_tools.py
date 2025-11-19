from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class GithubGqlClient:
    GH_ENDPOINT_URL = "https://api.github.com/graphql"

    def __init__(self, token):
        transport = RequestsHTTPTransport(
            url=self.GH_ENDPOINT_URL, headers={"Authorization": f"Bearer {token}"}
        )
        self.client = Client(transport=transport)

    def execute(self, query: str, **kwargs) -> dict:
        """
        Executes the given GraphQL query and returns the result as a dictionary.

        Args:
            query (str): The GraphQL query to execute.

        Returns:
            dict: The result of the query as a dictionary.
        """
        return self.client.execute(gql(query), variable_values=kwargs)

    def add_issue_to_project(self, project_id: str, issue_id: str) -> str:
        """
        Adds an issue to a project.

        Args:
            project_id (str): The ID of the project.
            issue_id (str): The ID of the issue.

        Returns:
            str: The ID of the item connecting issue and project
        """
        query = """
            mutation AddIssue($projectID: ID!, $issueID: ID!) {
                addProjectV2ItemById(input: {
                    projectId: $projectID
                    contentId: $issueID}) {
                item {
                    id
                }
            }
        }
        """
        result = self.execute(query, **{"projectID": project_id, "issueID": issue_id})
        return result["addProjectV2ItemById"]["item"]["id"]

    def add_sub_issue(self, parent_issue_id: str, sub_issue_id: str) -> None:
        """
        Adds a sub-issue relationship between two issues.

        Args:
            parent_issue_id (str): The node ID of the parent issue.
            sub_issue_id (str): The node ID of the sub-issue.
        """
        query = """
            mutation AddSubIssue($issueId: ID!, $subIssueId: ID!) {
                addSubIssue(input: {
                    issueId: $issueId,
                    subIssueId: $subIssueId
                }) {
                    subIssue {
                        id
                    }
                }
            }
        """
        self.execute(query, **{"issueId": parent_issue_id, "subIssueId": sub_issue_id})
