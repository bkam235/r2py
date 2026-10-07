---
id: base.attr
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.attr

## Guidance
Translate R `attr` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "42a0bad5", "r_snippet": "fooWidget <- function(data, name, ...) {\n      # ... process the data ...\n      params <- list(foo = data, bar = TRUE)\n      # customize toJSON() argument values\n      attr(params, 'TOJSON_ARGS') <- list(digits = 7, na = 'string')\n      htmlwidgets::createWidget(name, x = params, ...)\n    }", "py_snippet": "def fooWidget(data, name, **kwargs):\n    # ... process the data ...\n    params = {\"foo\": data, \"bar\": True}\n    \n    # In Python, custom JSON serialization for digits and NA handling \n    # is typically handled by the json.dumps encoder.\n    # We simulate the TOJSON_ARGS behavior here.\n    def custom_serializer(obj):\n        if pd.isna(obj):\n            return \"string\" # approximating na = 'string'\n        if isinstance(obj, float):\n            return round(obj, 7) # approximating digits = 7\n        raise TypeError(f\"Type {type(obj)} not serializable\")\n\n    # In a real shiny-python environment, createWidget would be handled by \n    # the specific widget's Python wrapper or by returning a UI element.\n    # Since htmlwidgets::createWidget is an R-specific constructor, \n    # we represent the resulting state as a dictionary/json object.\n    \n    return json.dumps(params, **kwargs, default=custom_serializer)", "score": 1.0, "script_id": "htmlwidgets__vignette__develop_advanced_chunk5.R", "n_calls": 1}
- {"r_hash": "c59a77c8", "r_snippet": "fooWidget <- function(data, name, ...) {\n      # ... process the data ...\n      params <- list(foo = data, bar = TRUE)\n      # customize the JSON serializer\n      attr(params, 'TOJSON_FUNC') <- MY_OWN_JSON_FUNCTION\n      htmlwidgets::createWidget(name, x = params, ...)\n    }", "py_snippet": "def MY_OWN_JSON_FUNCTION(obj):\n    # Implementation of the custom JSON serializer\n    return str(obj)\n\nclass MyCustomEncoder(json.JSONEncoder):\n    def default(self, obj):\n        try:\n            return super().default(obj)\n        except TypeError:\n            return MY_OWN_JSON_FUNCTION(obj)\n\ndef fooWidget(data, name, **kwargs):\n    # ... process the data ...\n    params = {'foo': data, 'bar': True}\n    \n    # In Python, instead of setting an attribute on the list, \n    # we pass the custom encoder to the json.dumps function.\n    # Since there is no direct 1:1 for htmlwidgets::createWidget, \n    # we simulate the creation of the widget configuration.\n    \n    widget_json = json.dumps(params, cls=MyCustomEncoder)\n    \n    # Return a structure that a frontend would use, simulating createWidget\n    return {\n        \"name\": name,\n        \"x\": widget_json,\n        \"options\": kwargs\n    }", "score": 1.0, "script_id": "htmlwidgets__vignette__develop_advanced_chunk8.R", "n_calls": 1}

## Edit Examples
(none)
