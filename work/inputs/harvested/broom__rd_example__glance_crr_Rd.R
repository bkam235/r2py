# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.crr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 18

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("cmprsk")) withAutoprint({ # examplesIf

library(cmprsk)

# time to loco-regional failure (lrf)
lrf_time <- rexp(100)
lrf_event <- sample(0:2, 100, replace = TRUE)
trt <- sample(0:1, 100, replace = TRUE)
strt <- sample(1:2, 100, replace = TRUE)

# fit model
x <- crr(lrf_time, lrf_event, cbind(trt, strt))

# summarize model fit with tidiers
tidy(x, conf.int = TRUE)
glance(x)
}) # examplesIf