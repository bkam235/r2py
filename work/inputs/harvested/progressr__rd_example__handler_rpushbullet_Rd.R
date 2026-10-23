# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: handler_rpushbullet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 9

suppressPackageStartupMessages(library(progressr))
pkg <- "RPushbullet"
if (requireNamespace(pkg, quietly = TRUE)) {

  handlers("rpushbullet")
  with_progress({ y <- slow_sum(1:10) })
  print(y)
  
}