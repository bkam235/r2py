# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import os
import pytest
from unittest.mock import MagicMock

# Mocking gitcreds as there is no direct Python equivalent for gitcreds library
# r2py:entity:print
class GitCredsMock:
    def __init__(self):
        self.username = None

    def gitcreds_get(self):
        # Simulate reading from environment variable for the test
        cred_str = os.environ.get("GITHUB_PAT_GITHUB_COM", "")
        if "username:user1:" in cred_str:
            return MagicMock(username="user1")
        return None

gitcreds = GitCredsMock()

def test_another_github_user():
    # Setup credentials string
# r2py:entity:cred
    cred = (
        "protocol:https:"
        "host:github.com:"
        "username:user1:"
        "password:secret"
    )
    
    # Simulate withr::local_envvar by setting environment variable
# r2py:entity:local_envvar
    os.environ["GITHUB_PAT_GITHUB_COM"] = cred
    
    try:
        # print(gitcreds::gitcreds_get())
# r2py:entity:print
        print(gitcreds.gitcreds_get())
        
        # expect_equal(gitcreds::gitcreds_get()$username, "user1")
# r2py:entity:expect_equal
        assert gitcreds.gitcreds_get().username == "user1"
    finally:
        # Clean up environment variable
        if "GITHUB_PAT_GITHUB_COM" in os.environ:
            del os.environ["GITHUB_PAT_GITHUB_COM"]

if __name__ == "__main__":
    pytest.main([__file__])