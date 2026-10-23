# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: utf8_nchar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 20

suppressPackageStartupMessages(library(cli))
# Grapheme example, emoji with combining characters. This is a single
# grapheme, consisting of five Unicode code points:
# * `\U0001f477` is the construction worker emoji
# * `\U0001f3fb` is emoji modifier that changes the skin color
# * `\u200d` is the zero width joiner
# * `\u2640` is the female sign
# * `\ufe0f` is variation selector 16, requesting an emoji style glyph
emo <- "\U0001f477\U0001f3fb\u200d\u2640\ufe0f"
cat(emo)

utf8_nchar(emo, "chars") # = graphemes
utf8_nchar(emo, "bytes")
utf8_nchar(emo, "width")
utf8_nchar(emo, "codepoints")

# For comparision, the output for width depends on the R version used:
nchar(emo, "chars")
nchar(emo, "bytes")
nchar(emo, "width")