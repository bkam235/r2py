# r2py crawler metadata
# package: highr
# source_type: rd_example
# topic: hilight.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\highr\help
# lines: 13

library(highr)
hilight("x=1 # assignment")

txt = c("a <- 1 # something", "c(y=\"world\", z=\"hello\")", "b=function(x=5) {",
    "for(i in 1:10) {
  if (i < x) print(i) else break}}", "z@child # S4 slot",
    "'special chars <>#$%&_{}'")
cat(hi_latex(txt), sep = "\n")
cat(hi_html(txt), sep = "\n")

# the markup data frames
highr:::cmd_latex
highr:::cmd_html