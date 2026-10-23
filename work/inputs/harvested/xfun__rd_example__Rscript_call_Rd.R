# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: Rscript_call.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
factorial(10)
# should return the same value
xfun::Rscript_call("factorial", list(10))

# the first argument can be either a character string or a function
xfun::Rscript_call(factorial, list(10))

# Run Rscript starting a vanilla R session
xfun::Rscript_call(factorial, list(10), options = c("--vanilla"))