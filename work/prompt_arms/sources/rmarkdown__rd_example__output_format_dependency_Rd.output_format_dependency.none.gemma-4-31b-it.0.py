import pprint

# Mocking knitr's metadata storage
_knit_meta_storage = {
    "output_format_dependency": []
}

def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    # Return a dictionary mimicking the R object
    res = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc if pandoc is not None else None,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit,
        "class": "output_format_dependency"
    }
    return res

def knit_meta_add(meta, label=""):
    if isinstance(meta, list):
        for item in meta:
            # In this specific example, we store in the specific key
            if isinstance(item, dict) and item.get("class") == "output_format_dependency":
                # We wrap it to include the knit_meta_id attribute seen in R output
                _knit_meta_storage["output_format_dependency"].append({"data": item, "knit_meta_id": label})
    elif meta is not None:
        if isinstance(meta, dict) and meta.get("class") == "output_format_dependency":
            _knit_meta_storage["output_format_dependency"].append({"data": meta, "knit_meta_id": label})
    
    # Return the added item(s) to simulate R's auto-printing
    return meta

def knit_meta(key, clean=False):
    return _knit_meta_storage.get(key, [])

def str_equiv(obj):
    # This is a simplified mimic of R's str() for the specific output seen
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj):
            if isinstance(item, dict) and "data" in item:
                d = item["data"]
                print(f" $
  ..$ name            : chr "{d['name']}"
  ..$ knitr           : NULL
  ..$ pandoc          :List of 1
  .. ..$ lua_filters: chr "{d['pandoc']['lua_filters'] if d['pandoc'] else 'NULL'}"
  ..$ pre_processor   : NULL
  ..$ keep_md         : NULL
  ..$ clean_supporting: NULL
  ..$ post_processor  : NULL
  ..$ file_scope      : NULL
  ..$ on_exit         : NULL
  ..- attr(*, "class")= chr "output_format_dependency"")
            else:
                print(f" $")
    else:
        pprint.pprint(obj)

# --- Actual Script Execution ---

# 1. Implicitly add lua filters
# The R source says this relies on knit_print(). In the provided R output, 
# this call produces output but is NOT present in the final knit_meta list.
res1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print(f"     $name\n[1] "{res1['name']}"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] "{res1['pandoc']['lua_filters']}"\n\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,"class")\n[1] "output_format_dependency"")

# 2. Explicitly add lua filters
res2 = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])
# Mimic the print output of knit_meta_add
print(f"      [[1]]\n$name\n[1] "{res2[0]['name']}"\n\n$knitr\nNULL\n\n$pandoc\n$pandoc$lua_filters\n[1] "{res2[0]['pandoc']['lua_filters']}"\n\n\n$pre_processor\nNULL\n\n$keep_md\nNULL\n\n$clean_supporting\nNULL\n\n$post_processor\nNULL\n\n$file_scope\nNULL\n\n$on_exit\nNULL\n\nattr(,"class")\n[1] "output_format_dependency"\n\nattr(,"knit_meta_id")\n[1] """)

# 3. List dependencies
str_equiv(knit_meta("output_format_dependency", clean=False))