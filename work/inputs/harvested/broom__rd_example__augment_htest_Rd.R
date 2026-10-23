# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.htest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 24

suppressPackageStartupMessages(library(broom))
tt <- t.test(rnorm(10))

tidy(tt)

# the glance output will be the same for each of the below tests
glance(tt)

tt <- t.test(mpg ~ am, data = mtcars)

tidy(tt)

wt <- wilcox.test(mpg ~ am, data = mtcars, conf.int = TRUE, exact = FALSE)

tidy(wt)

ct <- cor.test(mtcars$wt, mtcars$mpg)

tidy(ct)

chit <- chisq.test(xtabs(Freq ~ Sex + Class, data = as.data.frame(Titanic)))

tidy(chit)
augment(chit)