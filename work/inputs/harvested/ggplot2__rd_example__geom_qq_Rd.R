# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_qq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 22

suppressPackageStartupMessages(library(ggplot2))
df <- data.frame(y = rt(200, df = 5))
p <- ggplot(df, aes(sample = y))
p + stat_qq() + stat_qq_line()

# Use fitdistr from MASS to estimate distribution params:
# if (requireNamespace("MASS", quietly = TRUE)) {
#   params <- as.list(MASS::fitdistr(df$y, "t")$estimate)
# }
# Here, we use pre-computed params
params <- list(m = -0.02505057194115, s = 1.122568610124, df = 6.63842653897)
ggplot(df, aes(sample = y)) +
  stat_qq(distribution = qt, dparams = params["df"]) +
  stat_qq_line(distribution = qt, dparams = params["df"])

# Using to explore the distribution of a variable
ggplot(mtcars, aes(sample = mpg)) +
  stat_qq() +
  stat_qq_line()
ggplot(mtcars, aes(sample = mpg, colour = factor(cyl))) +
  stat_qq() +
  stat_qq_line()