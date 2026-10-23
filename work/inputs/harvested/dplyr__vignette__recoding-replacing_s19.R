# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: recoding-replacing_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\recoding-replacing.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
lookup <- tribble(
  ~from , ~to                 ,
      1 , "Strongly disagree" ,
      2 , "Disagree"          ,
      3 , "Neutral"           ,
      4 , "Agree"             ,
      5 , "Strongly agree"
)