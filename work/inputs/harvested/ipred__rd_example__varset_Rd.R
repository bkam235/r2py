# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: varset.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 6

suppressPackageStartupMessages(library(ipred))
theta90 <- varset(N = 1000, sigma = 0.1, theta = 90, threshold = 0)
theta0 <- varset(N = 1000, sigma = 0.1, theta = 0, threshold = 0)
par(mfrow = c(1, 2))
plot(theta0$intermediate)
plot(theta90$intermediate)