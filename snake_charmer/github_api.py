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

    def setup_labels(self):
        """
        function to setup labels for the repo to correctly
        interface with this action
        """

    def load_setup_py_file(self):
        """
        function to load the setup.py file from the calling
        repo
        """

    def push_setup_py_file(self, branch: str = ""):
        """
        function which force pushes the updated setup.py file
        to a given branch
        """
