# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: rbridge.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 5

suppressPackageStartupMessages(library(e1071))
# simulate a Brownian bridge on [0,1] and plot it

x <- rbridge()
plot(x,type="l")