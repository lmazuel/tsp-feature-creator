Do your query here: https://docs.github.com/en/graphql/overview/explorer

A few interesting links:
- https://docs.github.com/en/graphql/reference/objects
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects?tool=cli#updating-projects
- https://docs.github.com/en/graphql/guides/using-global-node-ids

To get all fields Node ID of project 636 in Azure:
```gql
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
}
```

Which gives :
```json
{
  "data": {
    "organization": {
      "projectV2": {
        "id": "PVT_kwDOAGhwUs4Aeqls",
        "fields": {
          "edges": [
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnDg",
                "name": "Title"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnDk",
                "name": "Assignees"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnWc",
                "name": "Due"
              }
            },
            {
              "node": {
                "id": "PVTSSF_lADOAGhwUs4AeqlszgUOnDo",
                "name": "Status"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnDs",
                "name": "Labels"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnDw",
                "name": "Linked pull requests"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnD0",
                "name": "Milestone"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnD4",
                "name": "Repository"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnEA",
                "name": "Tracks"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnEE",
                "name": "Tracked by"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnEI",
                "name": "Reviewers"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOnxM",
                "name": "Epic Link"
              }
            },
            {
              "node": {
                "id": "PVTSSF_lADOAGhwUs4AeqlszgUOo4E",
                "name": "Feature"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOpzc",
                "name": "Cost"
              }
            },
            {
              "node": {
                "id": "PVTSSF_lADOAGhwUs4AeqlszgUOqYk",
                "name": "Language"
              }
            },
            {
              "node": {
                "id": "PVTF_lADOAGhwUs4AeqlszgUOwSs",
                "name": "Spec Link"
              }
            },
            {
              "node": {
                "id": "PVTSSF_lADOAGhwUs4AeqlszgU1XyQ",
                "name": "Pri"
              }
            }
          ]
        }
      }
    }
  }
}
```

## Find an issue Node ID

```gql
{
  organization(login: "Azure") {
    repository(name: "autorest.python") {
      issue(number: 2482) {
        id
      }
    }
  }
}
```
gives:
```json
{
  "data": {
    "organization": {
      "repository": {
        "issue": {
          "id": "I_kwDOBfqzM86EZNq0"
        }
      }
    }
  }
}
```

## Red current values in an issue

```gql
{
  organization(login: "Azure") {
    repository(name: "autorest.python") {
      issue(number: 2482) {
        id
        projectItems(first: 1) {
          edges {
            node {            
              fieldValues(first: 20) {
                edges {
                  node {
                    ...on ProjectV2ItemFieldTextValue {
                      id
                      field {
                        ...on ProjectV2FieldCommon {
                          id
                          name
                        }
                      }
                      text
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```