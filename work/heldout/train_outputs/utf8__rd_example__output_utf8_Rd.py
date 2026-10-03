import os
import sys
import locale
import tempfile

def output_ansi():
    # R source: if (isatty(stdout())) { return(.Platform$GUI != "Rgui") }
    # To handle potential wrapped stdout (like _Tee), we check the original stdout
    target_stdout = sys.stdout
    if not hasattr(target_stdout, 'isatty'):
        target_stdout = sys.__stdout__
    
    try:
        if target_stdout.isatty():
            return True
    except Exception:
        pass
    
    # R source: if (!is.na(as.numeric(Sys.getenv("RSTUDIO_CONSOLE_COLOR")))) { return(stdout() == 1) }
    rstudio_color = os.environ.get("RSTUDIO_CONSOLE_COLOR")
    if rstudio_color is not None:
        try:
            float(rstudio_color)
            return True
        except ValueError:
            pass
            
    return False

def output_utf8():
    # R source: if (Sys.getlocale("LC_CTYPE") == "C") { return(FALSE) }
    try:
        # locale.setlocale(locale.LC_CTYPE, "C") in Python often results in 'C' or 'POSIX'
        curr_locale = locale.setlocale(locale.LC_CTYPE)
        if curr_locale in ("C", "POSIX"):
            return False
    except Exception:
        pass

    # R source: if (l10n_info()$`UTF-8`) { return(TRUE) }
    try:
        # Check if the current locale encoding is UTF-8
        # locale.getlocale can return ('en_US', 'UTF-8')
        loc_info = locale.getlocale(locale.LC_CTYPE)
        if loc_info and loc_info[1] and 'UTF-8' in loc_info[1].upper():
            return True
        # Fallback check on the locale name
        if loc_info and loc_info[0] and 'UTF-8' in loc_info[0].upper():
            return True
    except Exception:
        pass

    # R source: if (.Platform$OS.type == "windows") { return(TRUE) }
    if os.name == 'nt':
        return True
        
    return False

# r2py:entity:cat
def r_cat(*args, sep=' ', end=''):
    output = sep.join(map(str, args))
    sys.stdout.write(output + end)
    sys.stdout.flush()

def r_bool_str(val):
    return "TRUE" if val else "FALSE"

# Initial calls
r_cat("ANSI:", r_bool_str(output_ansi()), "\n")
# r2py:entity:cat_1
r_cat("UTF8:", r_bool_str(output_utf8()), "\n")

# Sys.setlocale("LC_CTYPE", "C")
# r2py:entity:Sys.setlocale
try:
    res = locale.setlocale(locale.LC_CTYPE, "C")
except locale.Error:
    res = locale.setlocale(locale.LC_CTYPE, "POSIX")
print(f'[1] "{res}"')

# r2py:entity:cat_2
r_cat("ANSI:", r_bool_str(output_ansi()), "\n")
# r2py:entity:cat_3
r_cat("UTF8:", r_bool_str(output_utf8()), "\n")

# Sys.setlocale("LC_CTYPE", "")
# r2py:entity:Sys.setlocale_1
try:
    res_native = locale.setlocale(locale.LC_CTYPE, "")
except locale.Error:
    res_native = "C"
print(f'[1] "{res_native}"')

# tmp <- tempfile()
# r2py:entity:tmp
tmp = tempfile.mktemp()

# sink(tmp)
# r2py:entity:sink
f_sink = open(tmp, "w", encoding="utf-8", newline='')
original_stdout = sys.stdout
sys.stdout = f_sink

# cat calls inside sink
# r2py:entity:cat_4
r_cat("ANSI:", r_bool_str(output_ansi()), "\n")
# r2py:entity:cat_5
r_cat("UTF8:", r_bool_str(output_utf8()), "\n")

# sink()
# r2py:entity:sink_1
sys.stdout.flush()
sys.stdout.close()
sys.stdout = original_stdout

# readLines(tmp)
# r2py:entity:readLines
with open(tmp, "r", encoding="utf-8") as f_in:
    lines = f_in.read().splitlines()

if not lines:
    print("character(0)")
else:
    formatted = ' '.join([f'"{l}"' for l in lines])
    print(f'[1] {formatted}')