# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: handler_beepr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 8

suppressPackageStartupMessages(library(progressr))
if (requireNamespace("beepr", quietly = TRUE)) {

  handlers("beepr")
  with_progress({ y <- slow_sum(1:10) })
  print(y)
  
}