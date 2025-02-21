from github.Issue import Issue

from tools import create_issue, create_task_list, get_repo, add_to_project, get_issue

PROD_MODE = True
AZURE_ONLY = False

if not PROD_MODE:
    # Testing
    TYPESPEC_EPIC_REPO = "lmazuel/typespec-azure"
    TYPESPEC_FEATURE_REPO = "lmazuel/typespec"
    TYPESPEC_CODEGEN_REPOS = [
        "lmazuel/autorest.python",
    ]
    TYPESPEC_SCENARIO_TEST_REPO = ("lmazuel/cadl-ranch", "lib:cadl-ranch")
    TCGC_REPO = "lmazuel/typespec-azure"
    PROJECT_NODE_ID = (
        "PVT_kwHOABAGLM4AfkOs"  # https://github.com/users/lmazuel/projects/1
    )
else:
    # Prod
    TYPESPEC_EPIC_REPO = "Azure/typespec-azure"
    TYPESPEC_FEATURE_REPO = "Microsoft/typespec"
    # Nice name: [prefix, repo, [labels]]
    TYPESPEC_CODEGEN_REPOS = {
        "Python": [
            "http-client-python",
            "Microsoft/typespec",
            ["emitter:client:python"],
        ],
        "Java": ["[http-client-java]", "Microsoft/typespec", ["emitter:client:java"]],
        "JS": ["[http-client-ts]", "Azure/autorest.typescript", ["CodeGen"]],
        "C#": ["[http-client-csharp]", "Microsoft/typespec", ["emitter:client:csharp"]],
        "Go": ["[http-client-go]", "Azure/autorest.go", ["TypeSpec", "CodeGen"]],
        "C++": ["[http-client-cpp]", "Azure/autorest.cpp", ["TypeSpec", "CodeGen"]],
        "Rust": ["[http-client-rust]", "Azure/typespec-rust", ["CodeGen"]],
    }
    TYPESPEC_SCENARIO_TEST_REPO = ("Azure/typespec-azure", "lib:azure-http-specs") if AZURE_ONLY else ("Microsoft/typespec", "lib:http-specs")
    TCGC_REPO = "Azure/typespec-azure"
    PROJECT_NODE_ID = (
        "PVT_kwDOAGhwUs4Aeqls"  # https://github.com/orgs/Azure/projects/636
    )


FEATURE_NAME = "Paging ContinuationToken"
NEED_USER_EXPERIENCE_ISSUE = False


def create_tsp_issue(feature_name: str, number: int = None) -> Issue:
    if number:
        issue = get_issue(TYPESPEC_FEATURE_REPO, number)
        add_to_project(PROJECT_NODE_ID, issue)
        return issue
    else:
        return create_issue(
            TYPESPEC_FEATURE_REPO,
            f"{feature_name} TSP Author doc",
            project_id=PROJECT_NODE_ID,
        )


def create_scenario_test_issue(feature_name):
    repo_name, label = TYPESPEC_SCENARIO_TEST_REPO
    return create_issue(
        repo_name,
        f"{feature_name} Scenario tests",
        project_id=PROJECT_NODE_ID,
        labels=[label],
    )


def create_codegen_issues(feature_name):
    user, impl = [], []
    for lang, metadata in TYPESPEC_CODEGEN_REPOS.items():
        prefix, repo_name, labels = metadata
        repo = get_repo(repo_name)

        if NEED_USER_EXPERIENCE_ISSUE:
            user.append(
                create_issue(
                    repo_name,
                    f"{prefix} {feature_name} User experience",
                    project_id=PROJECT_NODE_ID,
                    labels=labels,
                )
            )
        impl.append(
            create_issue(
                repo_name,
                f"{prefix} {feature_name} Implementation",
                project_id=PROJECT_NODE_ID,
                labels=labels,
            )
        )
    return user, impl


def create_tcgc_doc_issue(feature_name):
    return create_issue(
        TCGC_REPO,
        f"{feature_name} TCGC Author doc",
        project_id=PROJECT_NODE_ID,
        labels=["lib:tcgc", "docs"],
    )


def create_tcgc_issue(feature_name):
    return create_issue(
        TCGC_REPO,
        f"{feature_name} TCGC Implementation",
        project_id=PROJECT_NODE_ID,
        labels=["lib:tcgc"],
    )


def create_epic_issue(
    feature_name,
    tsp_issue: Issue | None,
    tsp_doc_issue: Issue,
    scenario_test_issue: Issue,
    user_experience_codegen_issues: list[Issue],
    implementation_issues: list[Issue],
    tcgc_issue: Issue,
) -> Issue:
    repo = get_repo(TYPESPEC_EPIC_REPO)
    body = ""

    if tsp_issue:
        body += create_task_list([tsp_issue], "TypeSpec")
        body += "\n\n"

    spec_list = [scenario_test_issue, tsp_doc_issue] + user_experience_codegen_issues
    if spec_list:
        body += create_task_list(spec_list, "Spec")
        body += "\n\n"

    body += create_task_list([tcgc_issue] + implementation_issues, "Implementation")

    issue = repo.create_issue(title=f"{feature_name}", body=body, labels=["Epic"])
    add_to_project(PROJECT_NODE_ID, issue)
    return issue


def create_all_issues(feature_name):
    tsp_spec = None  # create_tsp_issue(feature_name, 3736)
    user, impl = create_codegen_issues(feature_name)
    tcgc_doc = create_tcgc_doc_issue(feature_name)
    tcgc_impl = create_tcgc_issue(feature_name)
    cadl_ranch = create_scenario_test_issue(feature_name)
    issue = create_epic_issue(
        feature_name, tsp_spec, tcgc_doc, cadl_ranch, user, impl, tcgc_impl
    )
    print(f"Created issue: {issue.html_url}")
    print(f"Created issue: {issue.raw_data['node_id']}")


def do_it():
    create_all_issues(FEATURE_NAME)


if __name__ == "__main__":
    do_it()
