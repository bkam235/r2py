# r2py crawler metadata
# package: magrittr
# source_type: rd_example
# topic: compound.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\help
# lines: 21

suppressPackageStartupMessages(library(magrittr))
iris$Sepal.Length %<>% sqrt

x <- rnorm(100)

x %<>% abs %>% sort

is_weekend <- function(day)
{
   # day could be e.g. character a valid representation
   day %<>% as.Date
   
   result <- day %>% format("%u") %>% as.numeric %>% is_greater_than(5)
   
   if (result)
     message(day %>% paste("is a weekend!"))
   else
     message(day %>% paste("is not a weekend!"))
   
   invisible(result)
}