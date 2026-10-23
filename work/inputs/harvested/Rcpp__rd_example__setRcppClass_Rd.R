# r2py crawler metadata
# package: Rcpp
# source_type: rd_example
# topic: setRcppClass.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\Rcpp\help
# lines: 8

suppressPackageStartupMessages(library(Rcpp))
setRcppClass("World", 
    module = "yada", 
    fields = list(more = "character"),
    methods = list(
        test = function(what) message("Testing: ", what, "; ", more)),
    saveAs = "genWorld"
         )