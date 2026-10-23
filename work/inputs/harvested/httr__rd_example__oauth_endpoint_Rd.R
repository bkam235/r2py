# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: oauth_endpoint.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 13

suppressPackageStartupMessages(library(httr))
linkedin <- oauth_endpoint("requestToken", "authorize", "accessToken",
  base_url = "https://api.linkedin.com/uas/oauth"
)
github <- oauth_endpoint(NULL, "authorize", "access_token",
  base_url = "https://github.com/login/oauth"
)
facebook <- oauth_endpoint(
  authorize = "https://www.facebook.com/dialog/oauth",
  access = "https://graph.facebook.com/oauth/access_token"
)

oauth_endpoints