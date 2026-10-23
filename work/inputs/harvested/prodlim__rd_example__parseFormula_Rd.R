# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: parseFormula.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 36

suppressPackageStartupMessages(library(prodlim))
# Basic usage with specials
parseFormula(Y ~ fun(X, a = 1), specials = "fun")

# With defaults and aliases
parseFormula(Y ~ gfun(X, a = 7), 
             specials = "fun", 
             alias.names = list("fun" = "gfun"),
             special.default.values = list("fun" = list("a" = 0)))

# Complex use case with multiple specials
parseFormula(Surv(time, status) ~ age + strata(sex, test = 1) + prop(albumin),
             specials = c("prop", "strata"), 
             special.default.values = list("prop" = list(power = 0), "strata" = list(test = 1)))
parseFormula(Y~fun(X,a=1),specials="fun",special.default.values=list("fun"=list("a"=0)))
parseFormula(Y~fun(X),specials="fun",special.default.values=list("fun"=list("a"=0)))
parseFormula(Y~gfun(X,a=7),specials="fun",
             alias.names=list("fun"="gfun"),
             special.default.values=list("fun"=list("a"=0)))
parseFormula(formula = Surv(time,status)~age
                            +const(factor(edema))
                            +strata(sex,test=0)
                            +prop(alb)+prop(bili,power=1)
                            +tp(albumin),
                  specials = c("prop","timevar","strata","tp","const"),
                  special.default.values =list("prop" = list(power = 0),
                                               "strata" = list(test = 1)))
parseFormula(formula = Surv(time,status)~age
                            +const(factor(edema))
                            +strata(sex,test=0)
                            +prop(alb)+prop(bili,power=1)
                            +tp(albumin),
                  specials = c("prop","timevar","strata","tp"),
                  special.default.values =list("prop" = list(power = 0),
                                               "strata" = list(test = 1)),
                  alias.names=list("prop"="const"))