# r2py crawler metadata
# package: glue
# source_type: rd_example
# topic: glue_col.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\help
# lines: 34

suppressPackageStartupMessages(library(glue))
if (require(crayon)) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(crayon)

glue_col("{blue foo bar}")

glue_col("{blue 1 + 1 = {1 + 1}}")

glue_col("{blue 2 + 2 = {green {2 + 2}}}")

white_on_black <- bgBlack $ white
glue_col("{white_on_black
  Roses are {red {colors()[[552]]}},
  Violets are {blue {colors()[[26]]}},
  `glue_col()` can show \\
  {red c}{yellow o}{green l}{cyan o}{blue r}{magenta s}
  and {bold bold} and {underline underline} too!
}")

# this would error due to an unterminated quote, if we did not specify
# `.literal = TRUE`
glue_col("{yellow It's} happening!", .literal = TRUE)

# `.literal = TRUE` also prevents an error here due to the `#` comment
glue_col(
  "A URL: {magenta https://github.com/tidyverse/glue#readme}",
  .literal = TRUE
)

# `.literal = TRUE` does NOT prevent evaluation
x <- "world"
y <- "day"
glue_col("hello {x}! {green it's a new {y}!}", .literal = TRUE)
}) # examplesIf