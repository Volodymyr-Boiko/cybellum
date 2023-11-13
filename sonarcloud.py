import requests
from requests import HTTPError


class SonarCloudManager:
    def __init__(self):
        self.token = "42264a245bd9df77dd13a26e9bb04149e3423e19"

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def fetch_data_from_api(self, url, params):
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_project_status(self, project_name, **kwargs):
        url = "https://sonarcloud.io/api/qualitygates/project_status"
        params = {"projectKey": project_name, **kwargs}
        try:
            res = self.fetch_data_from_api(url, params=params)
        except HTTPError:
            print(f"Failed to fetch data from {url} for params: {params}")
            return None
        return res

    def fetch_project_pull_requests(self, project_name):
        url = "https://sonarcloud.io/api/project_pull_requests/list"
        return self.fetch_data_from_api(url, params={"project": project_name})

    def get_pr_number(self, project_name, branch, commit_sha):
        pr_list_json = self.fetch_project_pull_requests(project_name)
        for pr in pr_list_json.get("pullRequests"):
            # TODO: implement the case if commit was rewritten by next push
            if pr.get("branch") == branch and pr.get("commit").get("sha") == commit_sha:
                return pr.get("key")
        return None

    def fetch_report_by_branch(self, project_name, branch):
        return self.fetch_project_status(project_name, branch=branch)

    def fetch_report_by_pr(self, project_name, branch, commit_sha):
        pr_num = self.get_pr_number(project_name, branch, commit_sha)
        print(f"PR num: {pr_num}")
        if not pr_num:
            return None
        return self.fetch_project_status(project_name, pullRequest=pr_num)

    def fetch_report(self, project_name, branch, commit_sha):
        # the report is not created if commit was pushed to the branch, but PR was not created
        print("Fetch report by branch")
        report = self.fetch_report_by_branch(project_name, branch)
        if not report:
            print("Fetch report by pr")
            report = self.fetch_report_by_pr(project_name, branch, commit_sha)
        return report
