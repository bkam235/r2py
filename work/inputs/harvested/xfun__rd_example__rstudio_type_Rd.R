# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: rstudio_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

library(xfun)
if (loadable("rstudioapi") && rstudioapi::isAvailable()) {
    rstudio_type("Hello, RStudio! xfun::rstudio_type() looks pretty cool!",
        pause = function() runif(1, 0, 0.5), mistake = 0.1)
}