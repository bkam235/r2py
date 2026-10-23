# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: find_globals.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
x = 2
xfun::find_globals("y = x + 1")
xfun::find_globals("y = get('x') + 1")  # x is not recognized
xfun::find_globals("y = zzz + 1")  # zzz doesn't exist

xfun::find_locals("y = x + 1")
xfun::find_locals("assign('y', x + 1)")  # it works
xfun::find_locals("assign('y', x + 1, new.env())")  # still smart
xfun::find_locals("eval(parse(text = 'y = x + 1'))")  # no way