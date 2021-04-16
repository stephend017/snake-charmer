from snake_charmer.github_api import GithubAPI


class HookManager:
    @staticmethod
    def on_release(github_api: GithubAPI, token: str):
        """
        """

        if not github_api.has_on_release_hook():
            return

        hook = github_api.get_on_release_hook()

        # this file should be a python script that has a main method
        # and executes its given code when run
        # !! THIS IS NOT SAFE: I AM LAZY, USE THIS HOOK AT YOUR OWN RISK
        exec(hook, {"g_github_token": token})
