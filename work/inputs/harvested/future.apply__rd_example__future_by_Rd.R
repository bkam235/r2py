# r2py crawler metadata
# package: future.apply
# source_type: rd_example
# topic: future_by.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future.apply\help
# lines: 17

suppressPackageStartupMessages(library(future.apply))
## ---------------------------------------------------------
## by()
## ---------------------------------------------------------
library(datasets) ## warpbreaks
library(stats)    ## lm()

y0 <- by(warpbreaks, warpbreaks[,"tension"],
         function(x) lm(breaks ~ wool, data = x))

plan(multisession)
y1 <- future_by(warpbreaks, warpbreaks[,"tension"],
                function(x) lm(breaks ~ wool, data = x))

plan(sequential)
y2 <- future_by(warpbreaks, warpbreaks[,"tension"],
                function(x) lm(breaks ~ wool, data = x))