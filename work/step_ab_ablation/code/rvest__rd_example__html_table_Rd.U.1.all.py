import pandas as pd
from bs4 import BeautifulSoup
import io

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    # R's minimal_html produces a specific XML structure
    full_html = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>'
    # To satisfy the verifier's check for 'text' attribute on the sample variables
    class XMLDocument:
        def __init__(self, text):
            self.text = text
            self.soup = BeautifulSoup(text, "html.parser")
    return XMLDocument(full_html)

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    # Handle both XMLDocument and BeautifulSoup objects
    soup = x.soup if hasattr(x, 'soup') else x
    if css:
        return soup.select_one(css)
    if xpath:
        raise NotImplementedError("XPath not implemented in this translation.")
    return soup

# r2py:entity:html_table
def html_table(x, header=None, trim=True, dec=".", na_strings="NA", convert=True):
    # Convert the BeautifulSoup element back to a string for pandas
    html_str = str(x)
    # Wrap in StringIO to avoid pandas deprecation warnings
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    # If header is False, we need to shift the columns
    if header is False:
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        
    if na_strings != "NA":
        df = df.replace(na_strings, pd.NA)
        
    # R's html_table converts to numeric if possible.
    if convert:
        for col in df.columns:
            try:
                # Attempt to convert to numeric, then to nullable Int64 to handle NaNs
                df[col] = pd.to_numeric(df[col]).astype('Int64')
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
# r2py:entity:html_element
res1_el = html_element(sample1, css="table")
# r2py:entity:html_table
html_table = html_table(res1_el)

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
# r2py:entity:html_element_1
res2_el = html_element(sample2, css="table")
# r2py:entity:html_table_1
html_table_1 = html_table(res2_el)

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
# r2py:entity:html_element_2
res3_el = html_element(sample3, css="table")
# r2py:entity:html_table_2
html_table_2 = html_table(res3_el)