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
    
    def add_issue_to_project(self, project_id: int, issue_id: int) -> str:
        """
        Adds an issue to a project.

        Args:
            project_id (int): The ID of the project.
            issue_id (int): The ID of the issue.

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
        return result['addProjectV2ItemById']['item']['id']
