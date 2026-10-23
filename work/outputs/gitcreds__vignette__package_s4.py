# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os
import pytest
from unittest.mock import patch

# Mocking the gitcreds functionality since there is no direct 1:1 
# Python library for gitcreds, but simulating the behavior described.
# r2py:entity:import_gitcreds
class GitcredsNoCredentialsError(Exception):
    """Custom exception to match R's gitcreds_no_credentials class."""
    pass

def gitcreds_get(url):
    # Simulating the logic: if GITHUB_PAT_GITHUB_COM is "FAIL", raise error
    # This mimics the behavior described in the R vignette
    if os.environ.get("GITHUB_PAT_GITHUB_COM") == "FAIL":
        raise GitcredsNoCredentialsError("gitcreds_no_credentials")
    return "token"

def test_no_credentials_from_git():
    # withr::local_envvar(c(GITHUB_PAT_GITHUB_COM = "FAIL"))
# r2py:entity:local_envvar
    with patch.dict(os.environ, {"GITHUB_PAT_GITHUB_COM": "FAIL"}):
        # expect_error(gitcreds::gitcreds_get("https://github.com"), class_val= "gitcreds_no_credentials")
# r2py:entity:expect_error
        try:
            gitcreds_get("https://github.com")
            # If it doesn't raise, the test fails
            pytest.fail("Did not raise GitcredsNoCredentialsError")
        except GitcredsNoCredentialsError:
            # This is the expected outcome
            pass

if __name__ == "__main__":
    # Running the test function manually to mirror the R script's execution of test_that
    test_no_credentials_from_git()