# r2py crawler metadata
# package: gh
# source_type: rd_example
# topic: gh_gql.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gh\help
# lines: 19

suppressPackageStartupMessages(library(gh))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
gh_gql("query { viewer { login }}")

# Get rate limit
ratelimit_query <- "query {
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}"

gh_gql(ratelimit_query)
}) # examplesIf