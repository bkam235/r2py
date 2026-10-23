# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: magrittr_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\magrittr.R
# lines: 8

library(magrittr)

car_data <- 
  mtcars %>%
  subset(hp > 100) %>%
  aggregate(. ~ cyl, data = ., FUN = . %>% mean %>% round(2)) %>%
  transform(kpl = mpg %>% multiply_by(0.4251)) %>%
  print