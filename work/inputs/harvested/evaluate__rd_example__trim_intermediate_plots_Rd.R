# r2py crawler metadata
# package: evaluate
# source_type: rd_example
# topic: trim_intermediate_plots.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\evaluate\help
# lines: 11

suppressPackageStartupMessages(library(evaluate))
ev <- evaluate(c(
  "plot(1:3)",
  "text(1, 1, 'x')",
  "text(1, 1, 'y')"
))

# All intermediate plots are captured
ev
# Only the final plot is shown
trim_intermediate_plots(ev)