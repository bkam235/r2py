# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: as_sass.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 32

suppressPackageStartupMessages(library(sass))
# Example of regular Sass input
as_sass("body { color: \"blue\"; }")

# There is support for adding variables
as_sass(
  list(
    list(color = "blue"),
   "body { color: $color; }"
   )
)


# Add a file name
someFile <- tempfile("variables")

# Overwrite color to red
write("$color: \"red\";", someFile)

input <-
  as_sass(
    list(
      list(color = "blue"),
      sass_file(someFile),
      "body { color: $color; }"
      )
   )

input

# The final body color is red
sass(input)