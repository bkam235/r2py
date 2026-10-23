# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 4

suppressPackageStartupMessages(library(glue))
mini_mtcars <- head(cbind(model = rownames(mtcars), mtcars))
rownames(mini_mtcars) <- NULL
glue_data(mini_mtcars, "{model} has {hp} hp.")