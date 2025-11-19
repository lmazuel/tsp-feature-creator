from typing import cast
from github.Issue import Issue

from tools import create_issue, create_task_list, get_repo, add_to_project, get_issue, add_sub_issue

PROD_MODE = True
SCENARIO_TYPES = ("Generic", "Azure")  # Can be "Generic", "Azure", or both

if not PROD_MODE:
    # Testing
    TYPESPEC_EPIC_REPO = "lmazuel/typespec-azure"
    TYPESPEC_FEATURE_REPO = "lmazuel/typespec"
    TYPESPEC_CODEGEN_REPOS = {
        "Python": [
            "http-client-python",
            "lmazuel/autorest.python",
            ["test-label"],
        ],
    }
    TYPESPEC_SCENARIO_TEST_REPO = [("lmazuel/cadl-ranch", "lib:cadl-ranch")]
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
    # Determine scenario test repo based on SCENARIO_TYPES - always return a list
    TYPESPEC_SCENARIO_TEST_REPO = []
    if "Azure" in SCENARIO_TYPES:
        TYPESPEC_SCENARIO_TEST_REPO.append(("Azure/typespec-azure", "lib:azure-http-specs"))
    if "Generic" in SCENARIO_TYPES:
        TYPESPEC_SCENARIO_TEST_REPO.append(("Microsoft/typespec", "lib:http-specs"))
    if not TYPESPEC_SCENARIO_TEST_REPO:
        raise ValueError("SCENARIO_TYPES must contain at least 'Azure' or 'Generic'")
    TCGC_REPO = "Azure/typespec-azure"
    PROJECT_NODE_ID = (
        "PVT_kwDOAGhwUs4Aeqls"  # https://github.com/orgs/Azure/projects/636
    )


FEATURE_NAME = "Multiples services for one client"
FEATURE_TEXT = """Ability for emitters to generate one client from multiple services defined in TypeSpec.
Useful for ARM services like Compute where multiple services (VMs, Disks, Networks, etc.) are defined but a single client is expected.
"""
NEED_USER_EXPERIENCE_ISSUE = False


def create_tsp_issue(feature_name: str, number: int | None = None) -> Issue:
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
    # TYPESPEC_SCENARIO_TEST_REPO is always a list now
    issues = []
    for repo_name, label in TYPESPEC_SCENARIO_TEST_REPO:
        issues.append(create_issue(
            repo_name,
            f"{feature_name} Scenario tests",
            project_id=PROJECT_NODE_ID,
            labels=[label],
        ))
    return issues


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


def create_tcgc_issue(feature_name: str, number: int | None = None) -> Issue:
    if number:
        issue = get_issue(TCGC_REPO, number)
        add_to_project(PROJECT_NODE_ID, issue)
        return issue
    else:
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
    scenario_test_issues: list[Issue],
    user_experience_codegen_issues: list[Issue],
    implementation_issues: list[Issue],
    tcgc_issue: Issue,
    feature_text: str | None = None,
) -> Issue:
    repo = get_repo(TYPESPEC_EPIC_REPO)
    body = ""
    
    # Add feature text if provided
    if feature_text:
        body += feature_text
        body += "\n\n"

    if tsp_issue:
        body += create_task_list([tsp_issue], "TypeSpec")
        body += "\n\n"

    # scenario_test_issues is always a list now
    spec_list = scenario_test_issues + [tsp_doc_issue] + user_experience_codegen_issues
    if spec_list:
        body += create_task_list(cast(list[Issue | None], spec_list), "Spec")
        body += "\n\n"

    impl_list = [tcgc_issue] + implementation_issues
    body += create_task_list(cast(list[Issue | None], impl_list), "Implementation")

    issue = repo.create_issue(title=f"{feature_name}", body=body, labels=["Epic"])
    add_to_project(PROJECT_NODE_ID, issue)
    
    # Add all issues as sub-issues of the epic
    all_issues = []
    if tsp_issue:
        all_issues.append(tsp_issue)
    all_issues.extend(scenario_test_issues)
    all_issues.append(tsp_doc_issue)
    all_issues.extend(user_experience_codegen_issues)
    all_issues.append(tcgc_issue)
    all_issues.extend(implementation_issues)
    
    for sub_issue in all_issues:
        try:
            add_sub_issue(issue, sub_issue)
        except Exception as e:
            print(f"Warning: Could not add sub-issue {sub_issue.html_url}: {e}")
    
    return issue


def create_all_issues(feature_name):
    tsp_spec = None # create_tsp_issue(feature_name, 8874)
    user, impl = create_codegen_issues(feature_name)
    tcgc_doc = create_tcgc_doc_issue(feature_name)
    tcgc_impl = create_tcgc_issue(feature_name)
    cadl_ranch = create_scenario_test_issue(feature_name)
    issue = create_epic_issue(
        feature_name, tsp_spec, tcgc_doc, cadl_ranch, user, impl, tcgc_impl, FEATURE_TEXT
    )
    print(f"Created issue: {issue.html_url}")
    print(f"Created issue: {issue.raw_data['node_id']}")


def do_it():
    create_all_issues(FEATURE_NAME)


if __name__ == "__main__":
    do_it()
