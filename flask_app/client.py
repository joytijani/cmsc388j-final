import requests
import base64
import json

class Project(object):
    def __init__(self, github_json):
        self.title = github_json["name"]
        self.id = github_json["id"]
        self.url = github_json["html_url"]
        self.description = github_json["description"]

    def __repr__(self):
        return self.id


class ProjectClient(object):
    def __init__(self):
        self.sess = requests.Session()

    def fetch_projects(self,username):
        project_url = self.project_url = f"https://api.github.com/users/{username}/repos"
        resp = self.sess.get(project_url)
        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your Username is correct and authorized"
            )
        data = resp.json()

        if type(data) != list:
            raise ValueError(f'Error retrieving results: \'{data["Error"]}\' ')

        project = [Project(p_obj) for p_obj in data]
        return project
        
    def fetch_readme(self,username,title):
        project_url = self.project_url = f"https://api.github.com/repos/{username}/{title}/readme"
        resp = self.sess.get(project_url)
        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your Project Title is correct and authorized"
            )

        data = resp.json()
        print(type(data))
        data = base64.urlsafe_b64encode(json.dumps(data).encode()).decode('UTF-8')
        print(type(data))
        print(data)
        return data

    def fetch_project_by_id(self, username, project_id):
        project_url = self.project_url = f"https://api.github.com/users/{username}/repos"
        resp = self.sess.get(project_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your Project_ID is correct and authorized"
            )

        data = resp.json()

        if type(data) != list:
            raise ValueError(f'Error retrieving results: \'{data["Error"]}\' ')
        for p_obj in data:
            obj = Project(p_obj)
            if str(obj.id) == project_id:
                return obj
