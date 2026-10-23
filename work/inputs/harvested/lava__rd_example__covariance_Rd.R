# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: covariance.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 6

suppressPackageStartupMessages(library(lava))
m <- lvm()
### Define covariance between residuals terms of y1 and y2
covariance(m) <- y1~y2
covariance(m) <- c(y1,y2)~f(v) ## Same marginal variance
covariance(m) ## Examine covariance structure