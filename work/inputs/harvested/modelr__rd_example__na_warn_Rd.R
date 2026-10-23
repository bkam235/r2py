# r2py crawler metadata
# package: modelr
# source_type: rd_example
# topic: na.warn.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\modelr\help
# lines: 12

suppressPackageStartupMessages(library(modelr))
df <- tibble::tibble(
  x = 1:10,
  y = c(5.1, 9.7, NA, 17.4, 21.2, 26.6, 27.9, NA, 36.3, 40.4)
)
# Default behaviour is to silently drop
m1 <- lm(y ~ x, data = df)
resid(m1)

# Use na.action = na.warn to warn
m2 <- lm(y ~ x, data = df, na.action = na.warn)
resid(m2)