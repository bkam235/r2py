# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: new_pillar_component.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 5

suppressPackageStartupMessages(library(pillar))
new_pillar_component(list(letters[1:3]), width = 1)
pillar_component(new_pillar_title("letters"))
pillar_component(new_pillar_type(letters))
pillar_component(pillar_shaft(letters[1:3]))