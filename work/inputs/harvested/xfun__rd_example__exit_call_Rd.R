# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: exit_call.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
f = function(x) {
    print(x)
    xfun::exit_call(function() print("The parent function is exiting!"))
}
g = function(y) {
    f(y)
    print("f() has been called!")
}
g("An argument of g()!")