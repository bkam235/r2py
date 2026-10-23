# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: dystrophy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 6

suppressPackageStartupMessages(library(ipred))
data("dystrophy")
library("rpart")
errorest(Class~CK+H~AGE+PK+LD, data = dystrophy, model = inbagg, 
pFUN = list(list(model = lm, predict = mypredict.lm), list(model = rpart)), 
ns = 0.75, estimator = "cv")