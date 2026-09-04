---
id: testthat.expect-equal
package: testthat
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# testthat.expect-equal

## Guidance
Translate R `expect_equal` (FunctionCall from testthat) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8637e940", "r_snippet": "  expect_equal(dice(), 4)", "py_snippet": "    assert dice() == 4", "score": 1.0, "script_id": "auto"}
- {"r_hash": "3d164188", "r_snippet": "  expect_error(\n    gitcreds::gitcreds_get(\"https://github.com\"),\n    class = \"gitcreds_no_credentials\"\n  )", "py_snippet": "        try:\n            gitcreds_get(\"https://github.com\")\n            # If it doesn't raise, the test fails\n            pytest.fail(\"Did not raise GitcredsNoCredentialsError\")\n        except GitcredsNoCredentialsError:\n            # This is the expected outcome\n            pass\n\nif __name__ == \"__main__\":\n    # Running the test function manually to mirror the R script's execution of test_that\n    test_no_credentials_from_git()", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
