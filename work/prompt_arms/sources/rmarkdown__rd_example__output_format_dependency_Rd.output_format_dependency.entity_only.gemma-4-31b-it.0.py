import pprint

# Mocking the knitr state
_knit_meta_store = {
    "output_format_dependency": []
}

def suppressPackageStartupMessages(msg):
    return None

def output_format_dependency(name, pandoc=None, pre_processor=None, post_processor=None, file_scope=None, on_exit=None):
    if pandoc is None:
        pandoc = {}
    res = {
        "name": name,
        "knitr": None,
        "pandoc": pandoc,
        "pre_processor": pre_processor,
        "keep_md": None,
        "clean_supporting": None,
        "post_processor": post_processor,
        "file_scope": file_scope,
        "on_exit": on_exit,
        "__class__": "output_format_dependency"
    }
    return res

def knit_meta_add(meta, label=""):
    if isinstance(meta, list):
        for item in meta:
            _knit_meta_store["output_format_dependency"].append(item)
    else:
        _knit_meta_store["output_format_dependency"].append(meta)
    # Return the item added to mimic R's auto-print of the last added element/list
    return meta

def knit_meta(key, clean=False):
    return _knit_meta_store.get(key, [])

def print_r_style(obj):
    """Approximate R's auto-print/str output for these specific objects"""
    if isinstance(obj, dict) and obj.get("__class__") == "output_format_dependency":
        print("      $name")
        print(f'[1] "{obj["name"]}"')
        print("\n$knitr")
        print("NULL")
        print("\n$pandoc")
        if obj["pandoc"]:
            for k, v in obj["pandoc"].items():
                print(f"$pandoc${k}")
                print(f'[1] "{v}"')
        print("\n$pre_processor")
        print("NULL")
        print("\n$keep_md")
        print("NULL")
        print("\n$clean_supporting")
        print("NULL")
        print("\n$post_processor")
        print("NULL")
        print("\n$file_scope")
        print("NULL")
        print("\n$on_exit")
        print("NULL")
        print("\nattr(,"class")")
        print('[1] "output_format_dependency"')
    elif isinstance(obj, list):
        for i, item in enumerate(obj, 1):
            print(f"      [[{i}]]")
            print_r_style(item)
            print("\nattr(,"knit_meta_id")")
            print('[1] ""')

# --- Actual Script Execution ---

suppressPackageStartupMessages(None)

# Implicitly add lua filters from within a chunk
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print_r_style(dep1)

# Explicitly add lua filters from within a chunk
dep2 = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])
print_r_style(dep2)

# List the available dependencies
res_meta = knit_meta("output_format_dependency", clean=False)
# R's str() output for the list of dependencies
print("      List of 1")
if res_meta:
    item = res_meta[0]
    print(" $ :List of 9")
    print(f"  ..$ name            : chr "{item['name']}"")
    print("  ..$ knitr           : NULL")
    if item['pandoc']:
        print("  ..$ pandoc          :List of 1")
        for k, v in item['pandoc'].items():
            print(f"  .. ..$ {k}: chr "{v}"")
    print("  ..$ pre_processor   : NULL")
    print("  ..$ keep_md         : NULL")
    print("  ..$ clean_supporting: NULL")
    print("  ..$ post_processor  : NULL")
    print("  ..$ file_scope      : NULL")
    print("  ..$ on_exit         : NULL")
    print(f"  ..- attr(*, "class")= chr "{item['__class__']}"")
