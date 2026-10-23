# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.svyolr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 14

if (rlang::is_installed(c("survey", "MASS"))) withAutoprint({ # examplesIf
library(broom)
library(survey)

data(api)
dclus1 <- svydesign(id = ~dnum, weights = ~pw, data = apiclus1, fpc = ~fpc)
dclus1 <- update(dclus1, mealcat = cut(meals, c(0, 25, 50, 75, 100)))

m <- svyolr(mealcat ~ avg.ed + mobility + stype, design = dclus1)

m

tidy(m, conf.int = TRUE)
}) # examplesIf