# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: htmlPreserve.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 14

suppressPackageStartupMessages(library(htmltools))
# htmlPreserve will prevent "<script>alert(10*2*3);</script>"
# from getting an <em> tag inserted in the middle
markup <- paste(sep = "\n",
  "This is *emphasized* text in markdown.",
  htmlPreserve("<script>alert(10*2*3);</script>"),
  "Here is some more *emphasized text*."
)
extracted <- extractPreserveChunks(markup)
markup <- extracted$value
# Just think of this next line as Markdown processing
output <- gsub("\\*(.*?)\\*", "<em>\\1</em>", markup)
output <- restorePreserveChunks(output, extracted$chunks)
output