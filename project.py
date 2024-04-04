# Import necessary modules
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gh_token import GITHUB_TOKEN


# Define the GraphQL endpoint URL for GitHub
endpoint_url = "https://api.github.com/graphql"

# Create a transport using the requests library and set the authorization header
transport = RequestsHTTPTransport(url=endpoint_url, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"})

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define a GraphQL query to get repository information
query = gql("""
    query GetRepositories {
        viewer {
            repositories(first: 5) {
                nodes {
                    name
                    description
                    url
                }
            }
        }
    }
""")

# Execute the query on the transport
result = client.execute(query)

# Print the repository information
for repo in result["viewer"]["repositories"]["nodes"]:
    print(f"Repository: {repo['name']}")
    print(f"Description: {repo['description']}")
    print(f"URL: {repo['url']}\n")

# Note: Replace the query above with your specific requirements for GitHub data.

# Get the project ID for the TypeSpec project in the Azure organization
projectQuery = gql("""
query {
    organization(login: "Azure") {
        projectV2(number: 636) {
            id
        }
    }
}
""")
result = client.execute(projectQuery)
project_node_id = result["organization"]["projectV2"]["id"] # Actually for TypeSpec Framework, it's "PVT_kwDOAGhwUs4Aeqls"


projectQuery = gql("""
query {
    user(login: "lmazuel") {
        projectV2(number: 1) {
            id
        }
    }
}
""")
result = client.execute(projectQuery) # PVT_kwHOABAGLM4AfkOs"

addToProjectMutation = gql("""
mutation {
    addProjectV2ItemById(input: {
        projectId: "PVT_kwHOABAGLM4AfkOs"
        contentId: "I_kwDOKu2x2c6EixIT"}) {
      item {
        id
      }
    }
  }
""")
result = client.execute(addToProjectMutation)

projectQueryDetails = gql("""
query {
    organization(login: "Azure") {
        projectV2(number: 636) {
            id
            fields(first: 20) {
              edges {
                node {
                	...on ProjectV2FieldCommon {
                  	id
                    name
                  }
                }
              }
            }
        }
    }
}""")
result = client.execute(projectQueryDetails)

updateTextFieldMutation = gql("""
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PVT_kwDOAGhwUs4Aeqls",  # Project ID 
      itemId: "PVTI_lADOAGhwUs4AeqlszgN7rf0",  # ProjectV2Item, which is the entry of an issue in a project
      fieldId: "PVTF_lADOAGhwUs4AeqlszgUOwSs",
      value: {text: "Updated text"}}
  ) {
    projectV2Item {
      id
    }
  }
}
""")
result = client.execute(updateTextFieldMutation)