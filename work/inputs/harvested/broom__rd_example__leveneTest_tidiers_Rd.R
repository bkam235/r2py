# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: leveneTest_tidiers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 13

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("car")) withAutoprint({ # examplesIf

# load libraries for models and data
library(car)

data(Moore)

lt <- with(Moore, leveneTest(conformity, fcategory))

tidy(lt)
glance(lt)
}) # examplesIf