# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: knit_patterns.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 16

library(knitr)
opat = knit_patterns$get()  # old pattern list (to restore later)

apats = all_patterns  # a list of all built-in patterns
str(apats)
knit_patterns$set(apats[["rnw"]])  # set pattern list from apats

knit_patterns$get(c("chunk.begin", "chunk.end", "inline.code"))

# a customized pattern list; has to empty the original patterns first!
knit_patterns$restore()
# we may want to use this in an HTML document
knit_patterns$set(list(chunk.begin = "<!--helloR\\s+(.*)", chunk.end = "^byeR-->"))
str(knit_patterns$get())

knit_patterns$set(opat)  # put the old patterns back