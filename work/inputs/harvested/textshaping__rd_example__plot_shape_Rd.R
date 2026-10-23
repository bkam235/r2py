# r2py crawler metadata
# package: textshaping
# source_type: rd_example
# topic: plot_shape.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\textshaping\help
# lines: 11

suppressPackageStartupMessages(library(textshaping))
arab_text <- lorem_text("arabic", 2)
shape <- shape_text(
  arab_text,
  max_width = 5,
  indent = 0.2
)

try(
 plot_shape(shape)
)