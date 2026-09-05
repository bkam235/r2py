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
- {"r_hash": "54460bac", "r_snippet": "expect_s3_class(x1, 1)", "py_snippet": "def expect_s3_class(object, class_val, exact=False):\n    # Mimic the logic of R's expect_s3_class\n    # check_bool(exact)\n    if not isinstance(exact, bool):\n        raise TypeError(\"exact must be a boolean\")\n    \n    if class_val is None: # Handling NA equivalent\n        # S3 objects in Python aren't native, but we check if it's a custom object\n        if hasattr(object, '__class__'):\n            pytest.fail(\"Expected object not to be an S3 object.\")\n    elif isinstance(class_val, str):\n        # Simplified S3 class check: in Python, this is usually checking __class__.__name__ or isinstance\n ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
