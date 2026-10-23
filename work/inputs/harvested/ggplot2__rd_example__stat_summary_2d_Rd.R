# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_summary_2d.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
d <- ggplot(diamonds, aes(carat, depth, z = price))
d + stat_summary_2d()

# Specifying function
d + stat_summary_2d(fun = \(x) sum(x^2))
d + stat_summary_2d(fun = ~ sum(.x^2))
d + stat_summary_2d(fun = var)
d + stat_summary_2d(fun = "quantile", fun.args = list(probs = 0.1))

if (requireNamespace("hexbin")) {
d + stat_summary_hex()
d + stat_summary_hex(fun = ~ sum(.x^2))
}