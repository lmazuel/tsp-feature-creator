from github.Issue import Issue

from tools import create_issue, create_task_list, get_repo


TYPESPEC_EPIC_REPO = "lmazuel/typespec-azure"
TYPESPEC_FEATURE_REPO = "lmazuel/typespec"
TYPESPEC_CODEGEN_REPOS = [
    "lmazuel/autorest.python",
]
TYPESPEC_SCENARIO_TEST_REPO = "lmazuel/cadl-ranch"
TCGC_REPO = "lmazuel/typespec-azure"

FEATURE_NAME = "Streaming"


def create_tsp_issue(feature_name):
    return create_issue(TYPESPEC_FEATURE_REPO, f"{feature_name} TSP Author doc")


def create_scenario_test_issue(feature_name):
    return create_issue(TYPESPEC_SCENARIO_TEST_REPO, f"{feature_name} Scenario tests")


def create_codegen_issues(feature_name):
    user, impl = [], []
    for repo_name in TYPESPEC_CODEGEN_REPOS:
        repo = get_repo(repo_name)

        user.append(
            create_issue(repo_name, f"{feature_name} User experience")
        )
        impl.append(
            create_issue(repo_name, f"{feature_name} Implementation")
        )
    return user, impl


def create_tcgc_doc_issue(feature_name):
    return create_issue(TCGC_REPO, f"{feature_name} TCGC Author doc")


def create_tcgc_issue(feature_name):
    return create_issue(TCGC_REPO, f"{feature_name} TCGC Implementation")


def create_epic_issue(
    feature_name,
    tsp_issue: Issue,
    tsp_doc_issue: Issue,
    scenario_test_issue: Issue,
    user_experience_codegen_issues: list[Issue],
    implementation_issues: list[Issue],
    tcgc_issue: Issue,
):
    repo = get_repo(TYPESPEC_EPIC_REPO)

    body = create_task_list([tsp_issue], "TypeSpec")
    body += "\n\n"
    body += create_task_list(
        [scenario_test_issue, tsp_doc_issue] + user_experience_codegen_issues, "Spec"
    )
    body += "\n\n"
    body += create_task_list([tcgc_issue] + implementation_issues, "Implementation")

    issue = repo.create_issue(title=f"{feature_name}", body=body)
    return issue


def create_all_issues(feature_name):
    user, impl = create_codegen_issues(feature_name)
    tcgc_doc = create_tcgc_doc_issue(feature_name)
    tcgc_impl = create_tcgc_issue(feature_name)
    tsp_spec = create_tsp_issue(feature_name)
    cadl_ranch = create_scenario_test_issue(feature_name)
    issue = create_epic_issue(
        feature_name, tsp_spec, tcgc_doc, cadl_ranch, user, impl, tcgc_impl
    )
    print(f"Created issue: {issue.html_url}")


def do_it():
    create_all_issues(FEATURE_NAME)

if __name__ == "__main__":
    do_it()
    