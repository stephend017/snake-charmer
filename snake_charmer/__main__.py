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


if __name__ == "__main__":
    main()
