# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.binDesign.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 19

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("binGroup", "ggplot2"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(binGroup)

des <- binDesign(
  nmax = 300, delta = 0.06,
  p.hyp = 0.1, power = .8
)

glance(des)
tidy(des)

library(ggplot2)

ggplot(tidy(des), aes(n, power)) +
  geom_line()
}) # examplesIf