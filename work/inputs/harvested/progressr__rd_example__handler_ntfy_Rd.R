# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: handler_ntfy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 12

suppressPackageStartupMessages(library(progressr))
pkg <- "ntfy"
if (requireNamespace(pkg, quietly = TRUE)) {
  ## We need to specify a ntfy.sh topic that progress messages
  ## should be sent to. See help("ntfy_topic", package = "ntfy")
  ## for details
  Sys.setenv(NTFY_TOPIC = "R-my-secret-topic")

  handlers("ntfy")
  with_progress({ y <- slow_sum(1:10) })
  print(y)
}