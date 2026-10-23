# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: sass_partial.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 12

suppressPackageStartupMessages(library(sass))
theme <- sass_layer(
  defaults = sass_file(system.file("examples/variables.scss", package = "sass")),
  rules = sass_file(system.file("examples/rules.scss", package = "sass"))
)

# Compile the theme
sass(theme)

# Sometimes we want to use the variables from the theme to compile other sass
my_rules <- ".someclass { background-color: $bg; color: $fg; }"
sass_partial(my_rules, theme)