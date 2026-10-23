# r2py crawler metadata
# package: roxygen2
# source_type: rd_example
# topic: roclet_find.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\help
# lines: 14

suppressPackageStartupMessages(library(roxygen2))
# rd, namespace, and vignette work for backward compatibility
roclet_find("rd")

# But generally you should specify the name of a function that
# returns a roclet
roclet_find("rd_roclet")

# If it lives in another package, you'll need to use ::
roclet_find("roxygen2::rd_roclet")

# If it takes parameters (which no roclet does currently), you'll need
# to call the function
roclet_find("roxygen2::rd_roclet()")