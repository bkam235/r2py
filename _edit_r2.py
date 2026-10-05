from pathlib import Path
p = Path("r2py/stage0/effects/data.py")
s = p.read_text(encoding="utf-8")
old = '''        "  tryCatch({\n"
        f"{body}\n"
        "  }, error = function(e) '__uncapturable__')\n"
        "}\n"
'''
assert s.count(old) == 1
new = '''        "  .r2py_res <- tryCatch({\n"
        f"{body}\n"
        "  }, error = function(e) '__uncapturable__')\n"
        # A classed list with parts that cannot be captured (an xml2 document is a list of two external
        # pointers) says nothing as a dict: describe the whole object by its fingerprint instead.
        "  if (!is.null(attr(.r2py_obj, 'class')) && is.list(.r2py_res) && !is.data.frame(.r2py_obj) &&\n"
        "      .r2py_has_unc(.r2py_res)) {\n"
        "    .r2py_fp_res <- .r2py_fp(.r2py_obj)\n"
        "    if (!identical(.r2py_fp_res, '__uncapturable__')) return(.r2py_fp_res)\n"
        "  }\n"
        "  .r2py_res\n"
        "}\n"
'''
s = s.replace(old, new)
old2 = '''_R_FINGERPRINT_FN = (
'''
new2 = '''_R_FINGERPRINT_FN = (
    ".r2py_has_unc <- function(x) any(unlist(rapply(x, function(z) identical(z, '__uncapturable__'), how = 'list')))\n"
'''
assert s.count(old2) == 1
s = s.replace(old2, new2)
p.write_text(s, encoding="utf-8")
print("ok")
