# r2py crawler metadata
# package: miniUI
# source_type: rd_example
# topic: miniTitleBar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\miniUI\help
# lines: 5

suppressPackageStartupMessages(library(miniUI))
miniTitleBar("My App",
  left = miniTitleBarButton("prev", "Previous"),
  right = miniTitleBarButton("next", "Next")
)