from github.PullRequest import PullRequest
from github.Label import Label


class API:
    """
    Object to manage the different operations
    of this program
    """

    @staticmethod
    def on_pull_request_opened(pull_request: PullRequest):
        """
        Function that runs when a pull request is opened
        This is triggered by the action

        Args:
            pull_request (PullRequest): Full PR object from
                github API
        """

    @staticmethod
    def on_pull_request_labeled(pull_request: PullRequest, label: Label):
        """
        Function that runs when a pull request has a label
        added

        Args:
            pull_request (PullRequest): Full PR object from
                github API
            label (Label): the label that was added to the pull request
        """

    @staticmethod
    def on_pull_request_unlabeled(pull_request: PullRequest, label: Label):
        """
        Function that runs when a pull request has a label
        removed

        Args:
            pull_request (PullRequest): Full PR object from
                github API
            label (Label): the label that was removed to the pull request
        """

    @staticmethod
    def on_pull_request_merged(pull_request: PullRequest):
        """
        Function that runs when a pull request is merged

        Args:
            pull_request (PullRequest): Full PR object from
                github API
        """
