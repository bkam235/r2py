# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: click.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 12

suppressPackageStartupMessages(library(lava))
if (interactive()) {
    n <- 10; x <- seq(n); y <- runif(n)
    plot(y ~ x); click(x,y)

    data(iris)
    l <- lm(Sepal.Length ~ Sepal.Width*Species,iris)
    res <- plotConf(l,var2="Species")## ylim=c(6,8), xlim=c(2.5,3.3))
    with(res, click(x,y))

    with(iris, idplot(Sepal.Length,Petal.Length))
}