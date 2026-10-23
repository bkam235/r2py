# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: pal_hue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 16

suppressPackageStartupMessages(library(scales))
show_col(pal_hue()(4))
show_col(pal_hue()(9))
show_col(pal_hue(l = 90)(9))
show_col(pal_hue(l = 30)(9))

show_col(pal_hue()(9))
show_col(pal_hue(direction = -1)(9))
show_col(pal_hue(h.start = 30)(9))
show_col(pal_hue(h.start = 90)(9))

show_col(pal_hue()(9))
show_col(pal_hue(h = c(0, 90))(9))
show_col(pal_hue(h = c(90, 180))(9))
show_col(pal_hue(h = c(180, 270))(9))
show_col(pal_hue(h = c(270, 360))(9))