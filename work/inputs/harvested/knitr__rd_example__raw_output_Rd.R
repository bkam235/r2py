# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: raw_output.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 11

library(knitr)
out = c("*hello*", raw_output("<special>content</special> *protect* me!"),
    "*world*")
pre = extract_raw_output(out)
str(pre)
pre$value = gsub("[*]([^*]+)[*]", "<em>\\1</em>",
    pre$value)  # think this as Pandoc conversion
pre$value
# raw output was protected from the conversion
# (e.g. *protect* was not converted)
restore_raw_output(pre$value, pre$chunks)