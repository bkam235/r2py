# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: output_hooks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 8

suppressPackageStartupMessages(library(knitr))
# below is pretty much what knitr::render_markdown() does:
knitr::knit_hooks$set(knitr::hooks_markdown())

# you can retrieve a subset of the hooks and set them, e.g.,
knitr::knit_hooks$set(knitr::hooks_markdown()["source"])

knitr::knit_hooks$restore()