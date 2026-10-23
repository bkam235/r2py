# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: GlaucomaMVF.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 17

suppressPackageStartupMessages(library(ipred))
data("GlaucomaMVF", package = "ipred")
library("rpart")

response <- function (data) {
  attach(data)
  res <- ifelse((!is.na(clv) & !is.na(lora) & clv >= 5.1 & lora >= 
        49.23372) | (!is.na(clv) & !is.na(lora) & !is.na(cs) & 
        clv < 5.1 & lora >= 58.55409 & cs < 1.405) | (is.na(clv) & 
        !is.na(lora) & !is.na(cs) & lora >= 58.55409 & cs < 1.405) | 
        (!is.na(clv) & is.na(lora) & cs < 1.405), 0, 1)
  detach(data)
  factor (res, labels = c("glaucoma", "normal"))
}

errorest(Class~clv+lora+cs~., data = GlaucomaMVF, model=inclass, 
       estimator="cv", pFUN = list(list(model = rpart)), cFUN = response)