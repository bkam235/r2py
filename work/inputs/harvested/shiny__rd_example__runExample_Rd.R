# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: runExample.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 12

suppressPackageStartupMessages(library(shiny))
## Only run this example in interactive R sessions
if (interactive()) {
  # List all available examples
  runExample()

  # Run one of the examples
  runExample("01_hello")

  # Print the directory containing the code for all examples
  system.file("examples", package="shiny")
}