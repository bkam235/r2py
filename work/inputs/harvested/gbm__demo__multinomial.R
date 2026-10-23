# r2py crawler metadata
# package: gbm
# source_type: demo
# topic: multinomial
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gbm\demo\multinomial.R
# lines: 16

suppressPackageStartupMessages(library(gbm))
data( iris )
set.seed( 20090415 )

mod <- gbm(Species ~ ., 
           data              = iris, 
           distribution      = "multinomial",
           n.tree            = 5000, 
           shrinkage         = 0.001, 
           cv.folds          = 2,
           bag.fraction      = 0.8,
           interaction.depth = 3,
           verbose = FALSE)
gbm.perf( mod, method="cv" )
mod

