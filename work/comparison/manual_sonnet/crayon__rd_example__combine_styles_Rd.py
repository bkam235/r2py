# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: combine_styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 16

from rich.console import Console
from rich.style import Style

console = Console()

# Use style names (bold + dark_red + cyan background)
alert = Style(bold=True, color="dark_red", bgcolor="cyan")
console.print("Warning!", style=alert)

# Or style objects combined
bold = Style(bold=True)
red = Style(color="red")
bg_cyan = Style(bgcolor="cyan")
alert = bold + red + bg_cyan
console.print("Warning!", style=alert)

# Combine a composite style
alert = bold + (red + bg_cyan)
console.print("Warning!", style=alert)

# Shorter notation (chaining)
alert = Style.chain(bold, red, bg_cyan)
console.print("Warning!", style=alert)
