# r2py crawler metadata
# package: gh
# source_type: rd_example
# topic: gh.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gh\help
# lines: 85

suppressPackageStartupMessages(library(gh))
if (identical(Sys.getenv("IN_PKGDOWN"), "true")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Repositories of a user, these are equivalent
gh("/users/hadley/repos", .limit = 2)
gh("/users/{username}/repos", username = "hadley", .limit = 2)

## Starred repositories of a user
gh("/users/hadley/starred", .limit = 2)
gh("/users/{username}/starred", username = "hadley", .limit = 2)
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Create a repository, needs a token (see gh_token())
gh("POST /user/repos", name = "foobar")
}) # examplesIf
if (identical(Sys.getenv("IN_PKGDOWN"), "true")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Issues of a repository
gh("/repos/hadley/dplyr/issues")
gh("/repos/{owner}/{repo}/issues", owner = "hadley", repo = "dplyr")

## Automatic pagination
users <- gh("/users", .limit = 50)
length(users)
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Access developer preview of Licenses API (in preview as of 2015-09-24)
gh("/licenses") # used to error code 415
gh("/licenses", .accept = "application/vnd.github.drax-preview+json")
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Access Github Enterprise API
## Use GITHUB_API_URL environment variable to change the default.
gh("/user/repos", type = "public", .api_url = "https://github.foobar.edu/api/v3")
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Use I() to force body part to be sent as an array, even if length 1
## This works whether assignees has length 1 or > 1
assignees <- "gh_user"
assignees <- c("gh_user1", "gh_user2")
gh("PATCH /repos/OWNER/REPO/issues/1", assignees = I(assignees))
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## There are two ways to send JSON data. One is that you supply one or
## more objects that will be converted to JSON automatically via
## jsonlite::toJSON(). In this case sometimes you need to use
## jsonlite::unbox() because fromJSON() creates lists from scalar vectors
## by default. The Content-Type header is automatically added in this
## case. For example this request turns on GitHub Pages, using this
## API: https://docs.github.com/v3/repos/pages/#enable-a-pages-site

gh::gh(
  "POST /repos/{owner}/{repo}/pages",
  owner = "r-lib",
  repo = "gh",
  source = list(
    branch = jsonlite::unbox("gh-pages"),
    path = jsonlite::unbox("/")
  ),
  .send_headers = c(Accept = "application/vnd.github.switcheroo-preview+json")
)

## The second way is to handle the JSON encoding manually, and supply it
## as a raw vector in an unnamed argument, and also a Content-Type header:

body <- '{ "source": { "branch": "gh-pages", "path": "/" } }'
gh::gh(
  "POST /repos/{owner}/{repo}/pages",
  owner = "r-lib",
  repo = "gh",
  charToRaw(body),
  .send_headers = c(
    Accept = "application/vnd.github.switcheroo-preview+json",
    "Content-Type" = "application/json"
  )
)
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## Pass along a query to the search/code endpoint via the ... argument
x <- gh::gh(
            "/search/code",
            q = "installation repo:r-lib/gh",
            .send_headers = c("X-GitHub-Api-Version" = "2022-11-28")
            )
 str(x, list.len = 3, give.attr = FALSE)

}) # examplesIf