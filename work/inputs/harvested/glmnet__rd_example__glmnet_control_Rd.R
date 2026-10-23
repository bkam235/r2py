# r2py crawler metadata
# package: glmnet
# source_type: rd_example
# topic: glmnet.control.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\help
# lines: 4

suppressPackageStartupMessages(library(glmnet))
glmnet.control(fdev = 0)  #continue along path even though not much changes
glmnet.control()  # view current settings
glmnet.control(factory = TRUE)  # reset all the parameters to their default