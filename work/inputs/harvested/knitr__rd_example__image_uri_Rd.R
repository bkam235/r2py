# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: image_uri.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 6

suppressPackageStartupMessages(library(knitr))
uri = image_uri(file.path(R.home("doc"), "html", "logo.jpg"))
if (interactive()) {
    cat(sprintf("<img src=\"%s\" />", uri), file = "logo.html")
    browseURL("logo.html")  # you can check its HTML source
}