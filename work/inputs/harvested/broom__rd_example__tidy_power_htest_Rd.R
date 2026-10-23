# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.power.htest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 11

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("ggplot2")) withAutoprint({ # examplesIf

ptt <- power.t.test(n = 2:30, delta = 1)
tidy(ptt)

library(ggplot2)

ggplot(tidy(ptt), aes(n, power)) +
  geom_line()
}) # examplesIf