import re
from snake_charmer.hook_manager import HookManager
from github.Commit import Commit
from snake_charmer.models import VersionType
from snake_charmer.github_api import GithubAPI
from github.PullRequest import PullRequest
from github.Label import Label


class API:
    """
    Object to manage the different operations
    of this program
    """

    @staticmethod
    def on_pull_request_opened(
        github_api: GithubAPI, pull_request: PullRequest
    ):
        """
        Function that runs when a pull request is opened
        This is triggered by the action

        Args:
            github_api (GithubAPI): Wrapper object for interfacing
                with github
            pull_request (PullRequest): Full PR object from
                github API
        """
        did_add = github_api.setup_labels()
        if did_add:
            repo = github_api.get_repo()
            pr = repo.get_pull(pull_request["number"])
            pr.create_issue_comment(
                f"**`snake-charmer`** added new labels to this repository"
            )

    @staticmethod
    def on_pull_request_labeled(
        github_api: GithubAPI, pull_request: PullRequest, label: Label
    ):
        """
        Function that runs when a pull request has a label
        added

        Args:
            github_api (GithubAPI): Wrapper object for interfacing
                with github
            pull_request (PullRequest): Full PR object from
                github API
            label (Label): the label that was added to the pull request
        """
        github_api.load_setup_py_file(pull_request["head"]["ref"])
        labels = ["major-release", "minor-release", "revision-release"]
        labels.remove(label["name"])
        repo = github_api.get_repo()

        for l in pull_request["labels"]:
            if l["name"] == "beta" and label["name"] == "alpha":
                repo.get_pull(pull_request["number"]).remove_from_labels(
                    l["name"]
                )

            elif l["name"] == "alpha" and label["name"] == "beta":
                repo.get_pull(pull_request["number"]).remove_from_labels(
                    l["name"]
                )

            elif l["name"] in labels:
                # A release label that is not the one added
                # already exists. remove this label, update
                # setup.py

                # this is complicated because if we remove
                # a higher release for a lower one (minor
                # for major) the state is not recoverable
                # from the version itself (its not easy to
                # go from 0.1.0 to 0.0.7). We can fix this
                # by accessing the last commit where the
                # version was bumped from (since it
                # was committed)

                commits = repo.get_commits()
                index = 0
                while index < commits.totalCount:
                    commit: Commit = commits[index]

                    matches = re.findall(
                        r"Updated version to \d+\.\d+\.\d+",
                        commit.commit.message,
                    )
                    if len(matches) > 0:
                        commit_message = matches[len(matches) - 1]
                        version = commit_message[19:]
                        if version == github_api._get_setup_py_version()[1:-1]:
                            # don't look at the last version we added
                            index += 1
                            continue
                        github_api._setup_py = github_api._setup_py.replace(
                            github_api._get_setup_py_version()[1:-1], version
                        )
                        break
                    index += 1

                repo.get_pull(pull_request["number"]).remove_from_labels(
                    l["name"]
                )

        github_api.update_setup_py_file(VersionType.from_label(label["name"]))
        github_api.push_setup_py_file(pull_request["number"])

    @staticmethod
    def on_pull_request_unlabeled(
        github_api: GithubAPI, pull_request: PullRequest, label: Label
    ):
        """
        Function that runs when a pull request has a label
        removed

        Args:
            github_api (GithubAPI): Wrapper object for interfacing
                with github
            pull_request (PullRequest): Full PR object from
                github API
            label (Label): the label that was removed to the pull request
        """
        # no op if another label exists
        labels = ["major-release", "minor-release", "revision-release"]
        labels.remove(label["name"])
        for l in pull_request["labels"]:
            if l["name"] in labels:
                # no need to modify the version since label
                # metadata was updated when new version was added
                return

        github_api.load_setup_py_file(pull_request["head"]["ref"])
        github_api.update_setup_py_file(
            VersionType.from_label(label["name"]), increment=False
        )
        github_api.push_setup_py_file(pull_request["number"])

    @staticmethod
    def on_pull_request_merged(
        github_api: GithubAPI, pull_request: PullRequest, token: str
    ):
        """
        Function that runs when a pull request is merged

        Args:
            github_api (GithubAPI): Wrapper object for interfacing
                with github
            pull_request (PullRequest): Full PR object from
                github API
        """
        # generate changelog
        # create release
        defined_labels = ["major-release", "minor-release", "revision-release"]
        labels = pull_request["labels"]

        should_release = False
        is_beta = False
        is_alpha = False

        for label in labels:
            if label["name"] in defined_labels:
                should_release = True
            if label["name"] == "beta":
                is_beta = True
            if label["name"] == "alpha":
                is_alpha = True

        HookManager.on_release(github_api, token)

        if should_release:
            github_api.create_release(
                "main", is_beta=is_beta, is_alpha=is_alpha
            )
