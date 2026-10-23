# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: magrittr_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\magrittr.R
# lines: 6

suppressPackageStartupMessages(library(magrittr))
car_data <- 
  transform(aggregate(. ~ cyl, 
                      data = subset(mtcars, hp > 100), 
                      FUN = function(x) round(mean(x), 2)), 
            kpl = mpg*0.4251)