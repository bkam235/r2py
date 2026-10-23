# r2py crawler metadata
# package: ModelMetrics
# source_type: rd_example
# topic: mauc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ModelMetrics\help
# lines: 16

suppressPackageStartupMessages(library(ModelMetrics))
setosa <- glm(I(Species == 'setosa') ~ Sepal.Length, data = iris, family = 'binomial')
versicolor <- glm(I(Species == 'versicolor') ~ Sepal.Length, data = iris, family = 'binomial')
virginica <- glm(I(Species == 'virginica') ~ Sepal.Length, data = iris, family = 'binomial')

Pred <-
  data.frame(
    setosa = predict(setosa, type = 'response')
    ,versicolor = predict(versicolor, type = 'response')
    ,virginica = predict(virginica, type = 'response')
  )

Predicted = Pred/rowSums(Pred)
Actual = iris$Species

mauc(Actual, Predicted)