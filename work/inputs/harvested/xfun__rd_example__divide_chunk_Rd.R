# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: divide_chunk.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 11

suppressPackageStartupMessages(library(xfun))
# parse yaml-like items
yaml_like = c("#| label: mine", "#| echo: true", "#| fig.width: 8", "#| foo: bar",
    "1 + 1")
writeLines(yaml_like)
xfun::divide_chunk("r", yaml_like)

# parse CSV syntax
csv_like = c("#| mine, echo = TRUE, fig.width = 8, foo = 'bar'", "1 + 1")
writeLines(csv_like)
xfun::divide_chunk("r", csv_like)