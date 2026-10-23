# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: in_dir.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

library(xfun)
in_dir(tempdir(), {
    print(getwd())
    list.files()
})