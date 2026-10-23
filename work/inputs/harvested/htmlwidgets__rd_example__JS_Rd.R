# r2py crawler metadata
# package: htmlwidgets
# source_type: rd_example
# topic: JS.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmlwidgets\help
# lines: 4

library(htmlwidgets)
JS('1 + 1')
list(x = JS('function(foo) {return foo;}'), y = 1:10)
JS('function(x) {', 'return x + 1;', '}')