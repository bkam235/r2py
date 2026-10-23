# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knitr-intro
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knitr-intro.R
# lines: 14

suppressPackageStartupMessages(library(knitr))
options(digits = 4)
rnorm(20)
fit = lm(dist ~ speed, data = cars)
b = coef(fit)

summary(fit)$coefficients

par(mar=c(4, 4, 1, .1))
plot(cars, pch = 20)
abline(fit, col = 'red')

print(citation('knitr'), style = 'html')

