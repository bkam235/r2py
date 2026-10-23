# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: markdown.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 20

suppressPackageStartupMessages(library(shiny))
ui <- fluidPage(
  markdown("
    # Markdown Example

    This is a markdown paragraph, and will be contained within a `<p>` tag
    in the UI.

    The following is an unordered list, which will be represented in the UI as
    a `<ul>` with `<li>` children:

    * a bullet
    * another

    [Links](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a) work;
    so does *emphasis*.

    To see more of what's possible, check out [commonmark.org/help](https://commonmark.org/help).
    ")
)