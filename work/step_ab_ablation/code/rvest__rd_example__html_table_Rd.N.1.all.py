import pandas as pd
from bs4 import BeautifulSoup
import io

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return BeautifulSoup(full_html, "html.parser")

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    if css:
        return x.select_one(css)
    if xpath:
        raise NotImplementedError("XPath not implemented in this translation.")
    return x

# r2py:entity:html_table
def html_table(x, header=True, trim=True, dec=".", na_strings="NA", convert=True):
    # Convert the BeautifulSoup element back to a string for pandas
    html_str = str(x)
    # Wrap in StringIO to avoid pandas deprecation warnings
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    # R's html_table behavior:
    # If convert=True, it tries to guess types. Pandas read_html does this.
    # However, we need to make sure the result looks like a tibble (no index name)
    df.index.name = None
    
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
res1 = html_table(html_element(sample1, css="table"))
print(res1)

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
res2 = html_table(html_element(sample2, css="table"))
print(res2)

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
res3 = html_table(html_element(sample3, css="table"))
print(res3)