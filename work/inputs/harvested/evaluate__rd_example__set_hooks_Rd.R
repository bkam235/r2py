# r2py crawler metadata
# package: evaluate
# source_type: rd_example
# topic: set_hooks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\evaluate\help
# lines: 10

suppressPackageStartupMessages(library(evaluate))
new1 <- list(before.plot.new = function() print("Plotted!"))
new2 <- list(before.plot.new = function() print("Plotted Again!"))
set_hooks(new1)
set_hooks(new2)
plot(1)
remove_hooks(new1)
plot(1)
remove_hooks(new2)
plot(1)