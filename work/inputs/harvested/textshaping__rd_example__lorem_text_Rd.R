# r2py crawler metadata
# package: textshaping
# source_type: rd_example
# topic: lorem_text.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\textshaping\help
# lines: 9

suppressPackageStartupMessages(library(textshaping))
# Defaults to standard lorem ipsum
lorem_text()

# Get two paragraphs of hangul (Korean)
lorem_text("hangul", 2)

# Get gibberish bi-directional text
lorem_bidi()