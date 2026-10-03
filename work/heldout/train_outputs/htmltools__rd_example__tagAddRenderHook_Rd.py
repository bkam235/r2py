import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__tagAddRenderHook_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['divExtra', 'newObj', 'spanExtended', 'spanExtra', 'tags']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:obj
def dots_list(*args, **kwargs):
    # R's dots_list collects both positional and named arguments
    res = []
    for arg in args:
        res.append(arg)
    # For named args, we'll store them as a dict later in 'tag'
    return res, kwargs

def tag(tag_name, var_args, no_ws=None, render_hook=None):
    # var_args is (positional_list, named_dict)
    positional, named = var_args
    
    # Separate attributes (named) from children (unnamed)
    # In R's tag(), named args are attributes, positional are children
    attribs = named
    children = positional
    
    st = {
        "name": tag_name,
        "attribs": attribs,
        "children": children,
        ".renderHooks": []
    }
    
    if no_ws is not None:
        st[".noWS"] = no_ws
    
    if render_hook is not None:
        if not isinstance(render_hook, list):
            render_hook = [render_hook]
        st[".renderHooks"] = render_hook
        
    return st

def div(*args, no_ws=None, render_hook=None):
    contents = dots_list(*args)
    return tag("div", contents, no_ws=no_ws, render_hook=render_hook)

def strong(*args, no_ws=None, render_hook=None):
    contents = dots_list(*args)
    return tag("strong", contents, no_ws=no_ws, render_hook=render_hook)

def p(*args, no_ws=None, render_hook=None):
    contents = dots_list(*args)
    return tag("p", contents, no_ws=no_ws, render_hook=render_hook)

def tagAddRenderHook(tag_obj, func, replace=False):
    if replace:
        tag_obj[".renderHooks"] = [func]
    else:
        tag_obj[".renderHooks"].append(func)
    return tag_obj

def tagAppendAttributes(tag_obj, **kwargs):
    # Merge new attributes into existing ones
    tag_obj["attribs"].update(kwargs)
    return tag_obj

def tagAppendChildren(tag_obj, *args):
    # Append children to the children list
    tag_obj["children"].extend(list(args))
    return tag_obj

# r2py:entity:htmlDependencies(newDep)
def htmlDependency(name, version, src, meta=None, script=None, stylesheet=None, head=None, attachment=None, package=None, all_files=True):
    # src is typically a named list/dict in R
    return {
        "name": name,
        "version": str(version),
        "src": src if isinstance(src, dict) else {"file": src},
        "meta": meta,
        "script": script,
        "stylesheet": stylesheet,
        "head": head,
        "attachment": attachment,
        "package": package,
        "all_files": all_files,
        "class": "html_dependency"
    }

def attachDependencies(tag_obj, value, append=False):
    # Handle dependency attachment
    deps = value if isinstance(value, list) else [value]
    
    # Get current dependencies from attribute
    current_deps = tag_obj.get("html_dependencies", [])
    
    if append:
        tag_obj["html_dependencies"] = current_deps + deps
    else:
        tag_obj["html_dependencies"] = deps
    return tag_obj

def htmlDependencies(tag_obj):
    return tag_obj.get("html_dependencies", [])

def render_tag_recursive(tag_obj, indent=0):
    if isinstance(tag_obj, str):
        return tag_obj
    if not isinstance(tag_obj, dict) or "name" not in tag_obj:
        return str(tag_obj)
    
    # Copy to avoid mutating original during render
    working_tag = {k: (v.copy() if isinstance(v, (dict, list)) else v) 
                   for k, v in tag_obj.items()}
    
    # Apply render hooks
    for hook in working_tag.get(".renderHooks", []):
        result = hook(working_tag)
        if result is not None:
            # The hook can return a modified tag or a completely new tag
            working_tag = result
            if not isinstance(working_tag, dict) or "name" not in working_tag:
                return str(working_tag)

    # Construct HTML
    name = working_tag["name"]
    attrs = working_tag.get("attribs", {})
    attr_str = "".join([f' {k}="{v}"' for k, v in attrs.items()]) if attrs else ""
    
    children = working_tag.get("children", [])
    # Recursive render children
    child_html = "".join([render_tag_recursive(c, indent + 2) for c in children])
    
    # R's print(tag) often adds newlines for nested tags
    if children:
        # Simple approximation of R's formatted output
        inner = f"\n{' ' * (indent+2)}{child_html}\n{' ' * indent}"
        # This is tricky to match exactly; using a simpler version first
    
    return f"<{name}{attr_str}>{child_html}</{name}>"

# r2py:entity:renderTags
def renderTags(tag_obj):
    # findDependencies simplified
    def find_deps(t):
        if isinstance(t, dict):
            d = t.get("html_dependencies", [])
            for c in t.get("children", []):
                d += find_deps(c)
            return d
        return []
    
    deps = find_deps(tag_obj)
    return {"dependencies": deps, "html": render_tag_recursive(tag_obj)}

# --- Main Execution ---

# obj <- div("example", .renderHook = function(x) { x$name <- "span"; x })
def hook_span(x):
    x["name"] = "span"
    return x

obj = div("example", render_hook=hook_span)

# obj$name # "div"
# r2py:entity:print
print(obj["name"])

# print(obj) # Prints as a `span`
print(render_tag_recursive(obj))

# spanExtra <- tagAddRenderHook(obj, function(x) { tagAppendAttributes(x, class_val= "extra") })
# r2py:entity:spanExtra
def hook_extra(x):
    return tagAppendAttributes(x, class_="extra") # avoid keyword 'class'

# r2py:entity:spanExtra_1
spanExtra = tagAddRenderHook(obj, hook_extra)
print(render_tag_recursive(spanExtra))

# divExtra <- tagAddRenderHook(obj, replace = TRUE, function(x) { tagAppendAttributes(x, class_val= "extra") })
# r2py:entity:divExtra
def hook_extra_div(x):
    # R source: Replace previous render method. 
    # In R, this replaces .renderHooks. The hook itself doesn't change the tag name, 
    # but the first hook (which changed div to span) is gone.
    return tagAppendAttributes(x, class_="extra")

# r2py:entity:divExtra_1
divExtra = tagAddRenderHook(obj, hook_extra_div, replace=True)
print(render_tag_recursive(divExtra))

# spanExtended <- tagAddRenderHook(obj, function(x) { tagAppendChildren(x, " ", tags$strong("bold text")) })
# r2py:entity:spanExtended
def hook_extended(x):
    return tagAppendChildren(x, " ", strong("bold text"))

# r2py:entity:spanExtended_1
spanExtended = tagAddRenderHook(obj, hook_extended)
print(render_tag_recursive(spanExtended))

# newDep <- tagAddRenderHook(obj, function(x) { ... })
# r2py:entity:newDep
def hook_dep(x):
    fa = htmlDependency(
        "font-awesome", "4.5.0", {"href": "shared/font-awesome"},
        stylesheet="css/font-awesome.min.css")
    return attachDependencies(x, fa, append=True)

newDep = tagAddRenderHook(obj, hook_dep)

# htmlDependencies(newDep) <- ...
# r2py:entity:htmlDependencies(newDep)
jqueryui = htmlDependency(
    "jqueryui", "1.11.4", {"href": "shared/jqueryui"},
    script="jquery-ui.min.js")
# R uses a replacement operator for the attribute
newDep["html_dependencies"] = htmlDependencies(newDep) + [jqueryui]

# renderTags(newDep)$dependencies
# r2py:entity:renderTags
print(renderTags(newDep)["dependencies"])

# newObj <- tagAddRenderHook(obj, function(x) { tags$p("Something else") })
# r2py:entity:newObj
def hook_new_obj(x):
    return p("Something else")

# r2py:entity:newObj_1
newObj = tagAddRenderHook(obj, hook_new_obj)
print(render_tag_recursive(newObj))