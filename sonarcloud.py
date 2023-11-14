import os

import requests
from requests import HTTPError


class SonarCloudManager:
    def __init__(self):
        self.sonar_token = os.getenv("SONAR_TOKEN")
        self.git_token = os.getenv("GIT_TOKEN")

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.sonar_token}"}

    def fetch_data_from_sonar_api(self, url, params):
        response = requests.get(url, params=params, headers={"Authorization": f"Bearer {self.sonar_token}"})
        response.raise_for_status()
        return response.json()

    def fetch_project_status(self, project_name, **kwargs):
        url = "https://sonarcloud.io/api/qualitygates/project_status"
        params = {"projectKey": project_name, **kwargs}
        try:
            res = self.fetch_data_from_sonar_api(url, params=params)
        except HTTPError:
            print(f"Failed to fetch data from {url} for params: {params}")
            return None
        return res

    def get_pr_number(self, owner, repo, commit_sha):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"
        response = requests.get(url, headers={'X-GitHub-Api-Version': '2022-11-28', "Authorization": f"Bearer {self.git_token}"})
        response.raise_for_status()
        response_json = response.json()
        # TODO: what to do if there is more than 1 PR
        pr_num = response_json[0].get("number")
        return pr_num

    def fetch_report_by_branch(self, project_name, branch):
        return self.fetch_project_status(project_name, branch=branch)

    def fetch_report_by_pr(self, project_name, owner, repo, commit_sha):
        pr_num = self.get_pr_number(owner, repo, commit_sha)
        print(f"PR num: {pr_num}")
        if not pr_num:
            return None
        return self.fetch_project_status(project_name, pullRequest=pr_num)

    def fetch_report(self, project_name, owner, repo, branch, commit_sha):
        """
        project_name - Volodymyr-Boiko_cybellum
        owner - Volodymyr-Boiko
        repo - cybellum
        """
        # the report is not created if commit was pushed to the branch, but PR was not created
        print("Fetch report by branch")
        report = self.fetch_report_by_branch(project_name, branch)
        if not report:
            print("Fetch report by pr")
            report = self.fetch_report_by_pr(project_name, owner, repo, commit_sha)
        return report
