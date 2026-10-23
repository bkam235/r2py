# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.svyglm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 28

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("survey")) withAutoprint({ # examplesIf

# load libraries for models and data
library(survey)

set.seed(123)
data(api)

# survey design
dstrat <-
  svydesign(
    id = ~1,
    strata = ~stype,
    weights = ~pw,
    data = apistrat,
    fpc = ~fpc
  )

# model
m <- svyglm(
  formula = sch.wide ~ ell + meals + mobility,
  design = dstrat,
  family = quasibinomial()
)

glance(m)
}) # examplesIf