# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: combine_styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 16

from rich.style import Style
from rich.console import Console

console = Console()

# Use style names
alert = Style(bold=True, color="red", bgcolor="cyan")
console.print("Warning!", style=alert)

# Or combine styles
alert = Style(bold=True) + Style(color="red") + Style(bgcolor="cyan")
console.print("Warning!", style=alert)

# Combine a composite style
inner = Style(color="red") + Style(bgcolor="cyan")
alert = Style(bold=True) + inner
console.print("Warning!", style=alert)

# Shorter notation
alert = Style(bold=True, color="red", bgcolor="cyan")
console.print("Warning!", style=alert)
