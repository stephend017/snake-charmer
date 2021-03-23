import os
from snake_charmer.api import API
from sd_utils.github_actions.action import GithubAction


def main():
    """
    Basic algorithm

    3 modes (opened, labels & execute)

    opened:
        - runs when a PR is opened, checks that
          the correct labels exist, if not adds them

    labels:
        - runs when an open PR labels changes
            if label was added (update version)
            if label was removed decrement version
        - push setup.py file accordingly each time

    execute:
        - runs when labeled open PR is pushed.
        - generates changelog,
        - creates a new tag release with that defined
          in setup.py
        - pushes build to PYPI
    """
    action = GithubAction(
        "stephend017", "snake_charmer", os.environ, {"repository"}
    )

    event_payload = action.inputs["event_payload"]

    if "pull_request" in event_payload:
        if event_payload["action"] == "opened":
            API.on_pull_request_opened(event_payload["pull_request"])

        if event_payload["action"] == "labeled":
            API.on_pull_request_labeled(
                event_payload["pull_request"], event_payload["label"]
            )

        if event_payload["action"] == "unlabeled":
            API.on_pull_request_unlabeled(
                event_payload["pull_request"], event_payload["label"]
            )

        if event_payload["action"] == "closed":
            if event_payload["pull_request"]["merged"]:
                API.on_pull_request_merged(event_payload["pull_request"])


if __name__ == "__main__":
    main()
