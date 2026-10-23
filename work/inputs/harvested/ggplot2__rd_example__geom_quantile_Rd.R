# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_quantile.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 17

suppressPackageStartupMessages(library(ggplot2))
m <-
  ggplot(mpg, aes(displ, 1 / hwy)) +
  geom_point()
m + geom_quantile()
m + geom_quantile(quantiles = 0.5)
q10 <- seq(0.05, 0.95, by = 0.05)
m + geom_quantile(quantiles = q10)

# You can also use rqss to fit smooth quantiles
m + geom_quantile(method = "rqss")
# Note that rqss doesn't pick a smoothing constant automatically, so
# you'll need to tweak lambda yourself
m + geom_quantile(method = "rqss", lambda = 0.1)

# Set aesthetics to fixed value
m + geom_quantile(colour = "red", linewidth = 2, alpha = 0.5)