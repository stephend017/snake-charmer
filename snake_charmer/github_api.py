import json
import re
from github.PaginatedList import PaginatedList

from github.PullRequest import PullRequest
from github.Tag import Tag
from snake_charmer.models import VersionType
from github import Github
from github.Repository import Repository


class GithubAPI:
    """
    API for interfacing with a singular repo
    """

    def __init__(self, owner: str, repo: str, token: str):
        """
        """
        self._owner = owner
        self._repo = repo
        self._token = token
        self._github = Github(token)
        self._setup_py = ""
        self._test_sha = ""

    def setup_labels(self):
        """
        function to setup labels for the repo to correctly
        interface with this action
        """
        repo: Repository = self._get_repo()
        labels = repo.get_labels()
        with open("/assets/tags.json", "r") as fp:
            data = json.load(fp)
            for element in data:
                is_defined = False
                for label in labels:
                    if label.name == element["name"]:
                        is_defined = True
                if not is_defined:
                    repo.create_label(
                        element["name"],
                        element["color"],
                        element["description"],
                    )

    def load_setup_py_file(self, pr_ref: str):
        """
        function to load the setup.py file from the calling
        repo
        """
        repo = self._get_repo()
        response = repo.get_contents("setup.py", ref=pr_ref)
        self._setup_py = str(response.decoded_content, "utf-8")

    def update_setup_py_file(
        self, version_type: VersionType, increment: bool = True
    ):
        """
        """
        current_version = self._get_setup_py_version()
        value = 1 if increment else -1

        major_index = 1
        minor_index = current_version.find(".") + 1
        revision_index = current_version.find(".", minor_index) + 1

        major = int(current_version[major_index : minor_index - 1])
        minor = int(current_version[minor_index : revision_index - 1])
        revision = int(current_version[revision_index:-1])

        if version_type == VersionType.MAJOR:
            major += value
            minor = 0
            revision = 0
        if version_type == VersionType.MINOR:
            minor += value
            revision = 0
        if version_type == VersionType.REVISION:
            revision += value

        new_version = f'"{major}.{minor}.{revision}"'
        self._setup_py = self._setup_py.replace(current_version, new_version)

    def push_setup_py_file(self, number: int):
        """
        function which force pushes the updated setup.py file
        to a given branch
        """
        repo: Repository = self._get_repo()
        pr: PullRequest = repo.get_pull(number)
        sha = repo.get_contents("setup.py", pr.head.ref).sha
        repo.update_file(
            "setup.py",
            f"Updated version to {self._get_setup_py_version()[1:-1]}",
            self._setup_py,
            sha,
            pr.head.ref,
        )

    def create_release(self, ref: str):
        """
        Creates a release for the given branch
        """
        self.load_setup_py_file(ref)
        version = f"v{self._get_setup_py_version()[1:-1]}"
        repo = self._get_repo()
        # I think this is latest commit but not really sure
        sha = self._get_latest_commit_sha(ref)
        changelog = self._get_changelog()
        repo.create_git_tag_and_release(
            version,
            "\n".join(f"* {item}" for item in changelog),
            version,
            "\n".join(f"* {item}" for item in changelog),
            sha,
            "commit",
        )

    def _get_latest_commit_sha(self, ref: str):
        """
        """
        return self._get_repo().get_commits(ref).get_page(0)[0].sha

    def _get_changelog(self):
        """
        """
        repo = self._get_repo()
        commits = repo.get_commits()
        tags: PaginatedList[Tag] = repo.get_tags()
        stop_commit_sha = ""
        if tags.totalCount > 0:
            stop_commit_sha = tags[0].commit.sha

        changelog = []
        index = 0
        while commits[index].sha != stop_commit_sha:
            changelog.append(commits[index].commit.message)

            index += 1
            if index == commits.totalCount:
                break

        return changelog

    def _get_setup_py_version(self):
        """
        """
        return re.search(r'"\d\.\d\.\d"', self._setup_py).group()

    def _get_repo(self):
        """
        """
        return self._github.get_repo(f"{self._owner}/{self._repo}")
