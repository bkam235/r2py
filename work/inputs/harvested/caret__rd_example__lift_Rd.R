# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: lift.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 17

suppressPackageStartupMessages(library(caret))
set.seed(1)
simulated <- data.frame(obs = factor(rep(letters[1:2], each = 100)),
                        perfect = sort(runif(200), decreasing = TRUE),
                        random = runif(200))

lift1 <- lift(obs ~ random, data = simulated)
lift1
xyplot(lift1)

lift2 <- lift(obs ~ random + perfect, data = simulated)
lift2
xyplot(lift2, auto.key = list(columns = 2))

xyplot(lift2, auto.key = list(columns = 2), value = c(10, 30))

xyplot(lift2, plot = "lift", auto.key = list(columns = 2))