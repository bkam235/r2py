# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: learning_curve_dat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 22

suppressPackageStartupMessages(library(caret))
set.seed(1412)
class_dat <- twoClassSim(1000)

ctrl <- trainControl(classProbs = TRUE,
                     summaryFunction = twoClassSummary)

set.seed(29510)
lda_data <-
  learning_curve_dat(dat = class_dat,
                     outcome = "Class",
                     test_prop = 1/4,
                     ## `train` arguments:
                     method = "lda",
                     metric = "ROC",
                     trControl = ctrl)



ggplot(lda_data, aes(x = Training_Size, y = ROC, color = Data)) +
  geom_smooth(method = loess, span = .8) +
  theme_bw()