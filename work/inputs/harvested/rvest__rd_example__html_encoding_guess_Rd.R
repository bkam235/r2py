# r2py crawler metadata
# package: rvest
# source_type: rd_example
# topic: html_encoding_guess.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\help
# lines: 10

suppressPackageStartupMessages(library(rvest))
# A file with bad encoding included in the package
path <- system.file("html-ex", "bad-encoding.html", package = "rvest")
x <- read_html(path)
x |> html_elements("p") |> html_text()

html_encoding_guess(x)
# Two valid encodings, only one of which is correct
read_html(path, encoding = "ISO-8859-1") |> html_elements("p") |> html_text()
read_html(path, encoding = "ISO-8859-2") |> html_elements("p") |> html_text()