# r2py crawler metadata
# package: glue
# source_type: rd_example
# topic: glue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\help
# lines: 42

suppressPackageStartupMessages(library(glue))
name <- "Fred"
age <- 50
anniversary <- as.Date("1991-10-12")
glue('My name is {name},',
  'my age next year is {age + 1},',
  'my anniversary is {format(anniversary, "%A, %B %d, %Y")}.')

# single braces can be inserted by doubling them
glue("My name is {name}, not {{name}}.")

# Named arguments can be used to assign temporary variables.
glue('My name is {name},',
  ' my age next year is {age + 1},',
  ' my anniversary is {format(anniversary, "%A, %B %d, %Y")}.',
  name = "Joe",
  age = 40,
  anniversary = as.Date("2001-10-12"))

# `glue()` can also be used in user defined functions
intro <- function(name, profession, country){
  glue("My name is {name}, a {profession}, from {country}")
}
intro("Shelmith", "Senior Data Analyst", "Kenya")
intro("Cate", "Data Scientist", "Kenya")

# `glue_data()` is useful in magrittr pipes
if (require(magrittr)) {

mtcars %>% glue_data("{rownames(.)} has {hp} hp")

# Or within dplyr pipelines
if (require(dplyr)) {

head(iris) %>%
  mutate(description = glue("This {Species} has a petal length of {Petal.Length}"))

}}

# Alternative delimiters can also be used if needed
one <- "1"
glue("The value of $e^{2\\pi i}$ is $<<one>>$.", .open = "<<", .close = ">>")