# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: lvm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 5

suppressPackageStartupMessages(library(lava))
m <- lvm() # Empty model
m1 <- lvm(y~x) # Simple linear regression
m2 <- lvm(~y1+y2) # Model with two independent variables (argument)
m3 <- lvm(list(c(y1,y2,y3)~u,u~x+z)) # SEM with three items