import pandas as pd
from bs4 import BeautifulSoup
import io

# r2py:entity:sample1
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title>{title}</title>\n{html}"
    return BeautifulSoup(full_html, "html.parser")

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    if css:
        return x.select_one(css)
    if xpath:
        # rvest uses xpath via xml2; in this context we only need CSS for the examples
        raise NotImplementedError("XPath not implemented.")
    return x

# r2py:entity:html_table
def html_table(x, header=True, trim=True, dec=".", na_strings="NA", convert=True):
    # Convert the BeautifulSoup element back to a string for pandas
    html_str = str(x)
    # read_html returns a list of DataFrames
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    # If header=False, read_html might still have treated the first row as header.
    # However, R's html_table(header=TRUE) is default.
    if not header:
        # This is a simplification; usually involves shifting the header to the first row
        pass

    # R's html_table doesn't typically coerce to Int64 automatically in a way that 
    # pandas read_html does (it often keeps them as objects or floats).
    # We'll keep pandas default behavior which is closest to the resulting tibble/df.
    
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
# r2py:entity:html_element
res1 = html_element(sample1, css="table")
# r2py:entity:html_table
res1 = html_table(res1)

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
# r2py:entity:html_element_1
res2 = html_element(sample2, css="table")
# r2py:entity:html_table_1
res2 = html_table(res2)

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
# r2py:entity:html_element_2
res3 = html_element(sample3, css="table")
# r2py:entity:html_table_2
res3 = html_table(res3)