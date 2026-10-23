# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.nlrq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 22

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("ggplot2")) withAutoprint({ # examplesIf

# fit model
n <- nls(mpg ~ k * e^wt, data = mtcars, start = list(k = 1, e = 2))

# summarize model fit with tidiers + visualization
tidy(n)
augment(n)
glance(n)

library(ggplot2)

ggplot(augment(n), aes(wt, mpg)) +
  geom_point() +
  geom_line(aes(y = .fitted))

newdata <- head(mtcars)
newdata$wt <- newdata$wt + 1

augment(n, newdata = newdata)
}) # examplesIf