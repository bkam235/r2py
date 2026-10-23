# r2py crawler metadata
# package: downlit
# source_type: rd_example
# topic: downlit_html_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\downlit\help
# lines: 9

suppressPackageStartupMessages(library(downlit))
if (rlang::is_installed("xml2")) withAutoprint({ # examplesIf
node <- xml2::read_xml("<p><code>base::t()</code></p>")
node

# node is modified in place
downlit_html_node(node)
node
}) # examplesIf