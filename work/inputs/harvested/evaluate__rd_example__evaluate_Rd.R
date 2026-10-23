# r2py crawler metadata
# package: evaluate
# source_type: rd_example
# topic: evaluate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\evaluate\help
# lines: 15

suppressPackageStartupMessages(library(evaluate))
evaluate(c(
  "1 + 1",
  "2 + 2"
))

# Not that's there's a difference in output between putting multiple
# expressions on one line vs spreading them across multiple lines
evaluate("1;2;3")
evaluate(c("1", "2", "3"))

# This also affects how errors propagate, matching the behaviour
# of the R console
evaluate("1;stop(2);3")
evaluate(c("1", "stop(2)", "3"))