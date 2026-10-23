# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: data.frame_tidiers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 14

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("ggplot2")) withAutoprint({ # examplesIf

td <- tidy(mtcars)
td

glance(mtcars)

library(ggplot2)
# compare mean and standard deviation
ggplot(td, aes(mean, sd)) + geom_point() +
     geom_text(aes(label = column), hjust = 1, vjust = 1) +
     scale_x_log10() + scale_y_log10() + geom_abline()
}) # examplesIf