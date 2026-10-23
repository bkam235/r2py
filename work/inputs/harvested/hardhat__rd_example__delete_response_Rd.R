# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: delete_response.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 6

suppressPackageStartupMessages(library(hardhat))
framed <- model_frame(Species ~ Sepal.Width, iris)

attr(delete.response(framed$terms), "dataClasses")

attr(delete_response(framed$terms), "dataClasses")