import pprint

# Mocking the .knitEnv globally to mimic R's environment
class KnitEnv:
    def __init__(self):
        self.meta = []
        self.knit_meta_id = []

_knitEnv = KnitEnv()

# Helper function to print R-style objects
def print_r_style(obj):
    """Print an R object in R-like format."""
    if isinstance(obj, dict) and obj.get("__class__") == "output_format_dependency":
        print(f"$name")
        print(f'[1] "{obj["name"]}"')
        print()
        print(f"$knitr")
        print("NULL")
        print()
        print(f"$pandoc")
        if obj["pandoc"]:
            for key, value in obj["pandoc"].items():
                print(f"$pandoc${key}")
                print(f'[1] "{value}"')
        print()
        print(f"$pre_processor")
        print("NULL")
        print()
        print(f"$keep_md")
        print("NULL")
        print()
        print(f"$clean_supporting")
        print("NULL")
        print()
        print(f"$post_processor")
        print("NULL")
        print()
        print(f"$file_scope")
        print("NULL")
        print()
        print(f"$on_exit")
        print("NULL")
        print()
        print('attr(,"class")')
        print('[1] "output_format_dependency"')
    elif isinstance(obj, list):
        for i, item in enumerate(obj, 1):
            print(f"[[{i}]]")
            if isinstance(item, dict) and item.get("__class__") == "output_format_dependency":
                print(f"$name")
                print(f'[1] "{item["name"]}"')
                print()
                print(f"$knitr")
                print("NULL")
                print()
                print(f"$pandoc")
                if item["pandoc"]:
                    for key, value in item["pandoc"].items():
                        print(f"$pandoc${key}")
                        print(f'[1] "{value}"')
                print()
                print(f"$pre_processor")
                print("NULL")
                print()
                print(f"$keep_md")
                print("NULL")
                print()
                print(f"$clean_supporting")
                print("NULL")
                print()
                print(f"$post_processor")
                print("NULL")
                print()
                print(f"$file_scope")
                print("NULL")
                print()
                print(f"$on_exit")
                print("NULL")
                print()
                print('attr(,"class")')
                print('[1] "output_format_dependency"')
                if i < len(obj):
                    print()
                    print('attr(,"knit_meta_id")')
                    print('[1] ""')

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
    if meta:
        meta_list = meta if isinstance(meta, list) else [meta]
        _knitEnv.meta.extend(meta_list)
        _knitEnv.knit_meta_id.extend([label] * len(meta_list))
    return _knitEnv.meta

def knit_meta(key, clean=False):
    return [item for item in _knitEnv.meta if isinstance(item, dict)]

def str_equiv(obj):
    # Print str() output for the object
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, item in enumerate(obj, 1):
            print(f" $ :List of 9")
            if isinstance(item, dict) and item.get("__class__") == "output_format_dependency":
                print(f"  ..$ name            : chr \"{item['name']}\"")
                print(f"  ..$ knitr           : NULL")
                print(f"  ..$ pandoc          :List of {len(item['pandoc'])}")
                if item["pandoc"]:
                    for key, value in item["pandoc"].items():
                        print(f"  .. ..$ {key}: chr \"{value}\"")
                print(f"  ..$ pre_processor   : NULL")
                print(f"  ..$ keep_md         : NULL")
                print(f"  ..$ clean_supporting: NULL")
                print(f"  ..$ post_processor  : NULL")
                print(f"  ..$ file_scope      : NULL")
                print(f"  ..$ on_exit         : NULL")
                print(f'  ..- attr(*, "class")= chr "output_format_dependency"')

# Implicitly add lua filters from within a chunk
dep1 = output_format_dependency(
    "lua_filter1",
    pandoc={"lua_filters": "example1.lua"}
)
print_r_style(dep1)

# Explicitly add lua filters from within a chunk
result = knit_meta_add([output_format_dependency(
    "lua_filter2",
    pandoc={"lua_filters": "example2.lua"}
)])
print_r_style(result)

# List the available dependencies
str_equiv(knit_meta("output_format_dependency", clean=False))
