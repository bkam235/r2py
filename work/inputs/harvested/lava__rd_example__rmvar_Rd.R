# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: rmvar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 9

suppressPackageStartupMessages(library(lava))
m <- lvm()
addvar(m) <- ~y1+y2+x
covariance(m) <- y1~y2
regression(m) <- c(y1,y2) ~ x
### Cancel the covariance between the residuals of y1 and y2
cancel(m) <- y1~y2
### Remove y2 from the model
rmvar(m) <- ~y2