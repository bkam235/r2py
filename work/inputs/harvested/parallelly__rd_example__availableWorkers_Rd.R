# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: availableWorkers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 28

suppressPackageStartupMessages(library(parallelly))
message(paste("Available workers:",
        paste(sQuote(availableWorkers()), collapse = ", ")))


options(mc.cores = 2L)
message(paste("Available workers:",
        paste(sQuote(availableWorkers()), collapse = ", ")))



## Always use two workers on host 'n1' and one on host 'n2'
options(parallelly.availableWorkers.custom = function() {
  c("n1", "n1", "n2")
})
message(paste("Available workers:",
        paste(sQuote(availableWorkers()), collapse = ", ")))



## A 50% random subset of the available workers.
## Note that it is safe to call availableWorkers() here.
options(parallelly.availableWorkers.custom = function() {
  workers <- parallelly::availableWorkers()
  sample(workers, size = 0.50 * length(workers))
})
message(paste("Available workers:",
        paste(sQuote(availableWorkers()), collapse = ", ")))