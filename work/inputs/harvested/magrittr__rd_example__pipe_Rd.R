# r2py crawler metadata
# package: magrittr
# source_type: rd_example
# topic: pipe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\help
# lines: 36

suppressPackageStartupMessages(library(magrittr))
# Basic use:
iris %>% head

# Use with lhs as first argument
iris %>% head(10)

# Using the dot place-holder
"Ceci n'est pas une pipe" %>% gsub("une", "un", .)
  
# When dot is nested, lhs is still placed first:
sample(1:10) %>% paste0(LETTERS[.])

# This can be avoided:
rnorm(100) %>% {c(min(.), mean(.), max(.))} %>% floor

# Lambda expressions: 
iris %>%
{
  size <- sample(1:10, size = 1)
  rbind(head(., size), tail(., size))
}

# renaming in lambdas:
iris %>%
{
  my_data <- .
  size <- sample(1:10, size = 1)
  rbind(head(my_data, size), tail(my_data, size))
}

# Building unary functions with %>%
trig_fest <- . %>% tan %>% cos %>% sin

1:10 %>% trig_fest
trig_fest(1:10)