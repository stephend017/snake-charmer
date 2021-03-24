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
        github_api.setup_labels()

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
        github_api.load_setup_py_file(pull_request["head"]["ref"])
        github_api.update_setup_py_file(
            VersionType.from_label(label["name"]), increment=False
        )
        github_api.push_setup_py_file(pull_request["number"])

    @staticmethod
    def on_pull_request_merged(
        github_api: GithubAPI, pull_request: PullRequest
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
        github_api.create_release("main")
