# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: withr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 19

suppressPackageStartupMessages(library(withr))
getwd()
with_dir(tempdir(), getwd())
getwd()

Sys.getenv("WITHR")
with_envvar(c("WITHR" = 2), Sys.getenv("WITHR"))
Sys.getenv("WITHR")

with_envvar(c("A" = 1),
  with_envvar(c("A" = 2), action = "suffix", Sys.getenv("A"))
)

# local variants are best used within other functions
f <- function(x) {
  local_envvar(c("WITHR" = 2))
  Sys.getenv("WITHR")
}
Sys.getenv("WITHR")