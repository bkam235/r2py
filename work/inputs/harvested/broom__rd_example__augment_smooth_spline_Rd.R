# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.smooth.spline.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 17

suppressPackageStartupMessages(library(broom))
if (FALSE) withAutoprint({ # examplesIf

# fit model
spl <- smooth.spline(mtcars$wt, mtcars$mpg, df = 4)

# summarize model fit with tidiers
augment(spl, mtcars)

# calls original columns x and y
augment(spl)

library(ggplot2)
ggplot(augment(spl, mtcars), aes(wt, mpg)) +
  geom_point() +
  geom_line(aes(y = .fitted))
}) # examplesIf