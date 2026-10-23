# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: output_template.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 5

suppressPackageStartupMessages(library(sass))
sass("body {color: red}", output = output_template())

func <- output_template(basename = "foo", dirname = "bar-")
func(suffix = "baz")