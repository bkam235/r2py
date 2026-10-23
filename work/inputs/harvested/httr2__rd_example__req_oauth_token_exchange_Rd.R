# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_oauth_token_exchange.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 19

suppressPackageStartupMessages(library(httr2))
# List Google Cloud storage buckets using an OIDC token obtained
# from e.g. Microsoft Entra ID or Okta and federated to Google. (A real
# project ID and workforce pool would be required for this in practice.)
#
# See: https://cloud.google.com/iam/docs/workforce-obtaining-short-lived-credentials
oidc_token <- "an ID token from Okta"
request("https://storage.googleapis.com/storage/v1/b?project=123456") |>
  req_oauth_token_exchange(
    client = oauth_client("gcp", "https://sts.googleapis.com/v1/token"),
    subject_token = oidc_token,
    subject_token_type = "urn:ietf:params:oauth:token-type:id_token",
    scope = "https://www.googleapis.com/auth/cloud-platform",
    requested_token_type = "urn:ietf:params:oauth:token-type:access_token",
    audience = "//iam.googleapis.com/locations/global/workforcePools/123/providers/456",
    token_params = list(
      options = '{"userProject":"123456"}'
    )
  )