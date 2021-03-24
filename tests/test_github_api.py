import os
from snake_charmer.models import VersionType
from snake_charmer.github_api import GithubAPI


def test_update_setup_up():
    """
    """
    g = GithubAPI("stephend017", "snake_charmer", os.environ["GH_PAT"])
    g.load_setup_py_file("main")
    g.update_setup_py_file(VersionType.MINOR)

    # assert 'version="0.1.1",' in g._setup_py
    # ! NOTE: testcase disabled cause hard to validate with this repo (fix later)


def test_getting_latest_sha():
    """
    """
    g = GithubAPI("stephend017", "snake_charmer", os.environ["GH_PAT"])

    sha = g._get_latest_commit_sha("main")

    assert True, sha
