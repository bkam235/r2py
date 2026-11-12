import pandas as pd
from bs4 import BeautifulSoup
import io

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    # rvest::minimal_html produces a full document structure
    full_html = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
        '<meta charset="utf-8">\n'
        f'<title>{title}</title>\n'
        "</head>\n"
        f"<body>{html}</body>\n"
        "</html>"
    )
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
    
    # If header is False, pandas read_html might have used the first row as columns
    # but rvest's html_table(header=FALSE) expects them as data.
    if header is False:
        # This is a simplification; real rvest header=FALSE handling is more complex
        df.columns = range(df.shape[1])
        
    if na_strings != "NA":
        df = df.replace(na_strings, pd.NA)
        
    # R's html_table converts to numeric if possible. 
    # To match R's tibble output (which uses integers where possible),
    # we try to convert to nullable integers.
    if convert:
        for col in df.columns:
            try:
                # Try numeric conversion, then to nullable Int64 if it looks like an integer
                s = pd.to_numeric(df[col])
                if (s.dropna() % 1 == 0).all():
                    df[col] = s.astype('Int64')
                else:
                    df[col] = s
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
# r2py:entity:html_element
res1_elem = html_element(sample1, css="table")
# r2py:entity:html_table
res1 = html_table(res1_elem)
print(res1)

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
# r2py:entity:html_element_1
res2_elem = html_element(sample2, css="table")
# r2py:entity:html_table_1
res2 = html_table(res2_elem)
print(res2)

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
# r2py:entity:html_element_2
res3_elem = html_element(sample3, css="table")
# r2py:entity:html_table_2
res3 = html_table(res3_elem)
print(res3)