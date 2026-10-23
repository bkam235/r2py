# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: engine_output.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 10

library(knitr)
engine_output(opts_chunk$merge(list(engine = "Rscript")),
    code = "1 + 1", out = "[1] 2")
engine_output(opts_chunk$merge(list(echo = FALSE, engine = "Rscript")),
    code = "1 + 1", out = "[1] 2")

# expert use only
engine_output(opts_chunk$merge(list(engine = "python")),
    out = list(structure(list(src = "1 + 1"), class = "source"),
        "2"))