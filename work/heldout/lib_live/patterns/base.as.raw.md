---
id: base.as.raw
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.as.raw

## Guidance
Translate R `as.raw` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5b6f0e7e", "r_snippet": "dataURI(as.raw(1:10)) # default is base64", "py_snippet": "def dataURI(data=None, mime=\"\", encoding=\"base64\", file=None):\n    if encoding is not None and encoding != \"base64\":\n        raise ValueError(\"encoding must be either None or \\\"base64\\\"\")\n    \n    prefix = f\"data:{mime}\"\n    if encoding is not None:\n        prefix += \";base64\"\n    prefix += \",\"\n\n    if file is not None:\n        if data is not None:\n            raise ValueError(\"data and file are mutually exclusive\")\n        with open(file, \"rb\") as f:\n            data = f.read()\n\n    if data is None:\n        data = b\"\"\n    \n    if not isinstance(data, (bytes, bytearray)):\n        if isinstance(data, (list, np.ndarray)):\n            # R's paste(as.character(data), collapse=\"\\n\")\n            data = \"\\n\".join(map(str, data.flatten())).encode(\"utf-8\")\n        else:\n            data = str(data).encode(\"utf-8\")\n\n    if encoding is None:\n        # R's C_URIencode (RFC 3986) uses %XX. quote() is closer than quote_plus()\n        encoded_data = urllib.parse.quote(data)\n    else:\n        encoded_data = base64.b64encode(data).decode(\"utf-8\")\n        \n    return prefix + encoded_data\n\ndata_raw = bytes(range(1, 11))\nprint(dataURI(data=data_raw)) \n\n# dataURI(as.raw(1:10), encoding=NULL)", "score": 1.0, "script_id": "base64enc__rd_example__dataURI_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "print(dataURI(data=data_raw, encoding=None)) # URI\n\ntry:\n    # Simulate 'require(\"png\")'\n    import PIL\n    # let's say you have an image - e.g. from dev.capture(TRUE)", "new_code": "print(dataURI(data=data_raw, encoding=None))\n\ntry:\n    # Simulate require(\"png\")\n    import PIL\n    # img <- matrix(1:16/16, 4) \n    # R fills by column: [1, 5, 9, 13], [2, 6, 10, 14]...\n    # r2py:entity:img", "score_delta": 0.2, "script_id": "base64enc__rd_example__dataURI_Rd", "r_snippet": "  dataURI(as.raw(1:10), encoding=NULL) # URI", "functions": ["base::as.raw"]}
