# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: as_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 15

suppressPackageStartupMessages(library(forcats))
# Character object
x <- c("a", "z", "g")
as_factor(x)
as.factor(x)

# Character object containing numbers
y <- c("1.1", "11", "2.2", "22")
as_factor(y)
as.factor(y)

# Numeric object
z <- as.numeric(y)
as_factor(z)
as.factor(z)