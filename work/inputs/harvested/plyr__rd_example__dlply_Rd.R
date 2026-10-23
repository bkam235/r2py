# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: dlply.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 11

suppressPackageStartupMessages(library(plyr))
linmod <- function(df) {
  lm(rbi ~ year, data = mutate(df, year = year - min(year)))
}
models <- dlply(baseball, .(id), linmod)
models[[1]]

coef <- ldply(models, coef)
with(coef, plot(`(Intercept)`, year))
qual <- laply(models, function(mod) summary(mod)$r.squared)
hist(qual)