# r2py crawler metadata
# package: downlit
# source_type: rd_example
# topic: downlit_md_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\downlit\help
# lines: 11

suppressPackageStartupMessages(library(downlit))
if (rlang::is_installed("rmarkdown")) withAutoprint({ # examplesIf
if (rmarkdown::pandoc_available("1.19")) {
downlit_md_string("`base::t()`")
downlit_md_string("`base::t`")
downlit_md_string("* `base::t`")

# But don't highlight in headings
downlit_md_string("## `base::t`")
}
}) # examplesIf