# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: sass_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 16

suppressPackageStartupMessages(library(sass))
x <- "foo { margin: 122px * .001; }"
sass(x)

# Provide options directly to sass()
sass(x, options = sass_options(precision = 1, output_style = "compact"))

# Or set some option(s) globally
old_options <- sass_options_set(precision = 1)
sass(x)

# Specify local options  while also respecting global options
sass(x, options = sass_options_get(output_style = "compact"))

# Restore original state
sass_options_set(old_options)