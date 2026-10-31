"""The Python capture of objects: no warnings of its own, and a callable object keeps its text form (2026-10-31).

The fingerprint walker reads every public attribute, which fired library DeprecationWarnings (bs4's ``nextSibling``,
``co_lnotab``) that were counted as the program's; a ``BeautifulSoup`` is callable (``__call__`` is ``find_all``), so
it was stored as a function's metadata, and R's XML document had "no text form" to compare with."""
from r2py.types import EffectClass


def _run(src):
    from r2py.stage0.sandbox.isolation import TempWorkdir
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    with TempWorkdir() as wd:
        return PySandbox().run(src, workdir=wd, capture=frozenset({EffectClass.DATA, EffectClass.WARNINGS}))


SOUP = "from bs4 import BeautifulSoup\nhtml = BeautifulSoup('<p>Hello <b>Hadley</b></p>', 'html.parser')\n"


def test_capture_makes_no_warnings():
    assert _run(SOUP).warnings == []


def test_program_warnings_still_captured():
    assert _run("import warnings\n" + SOUP + "warnings.warn('my own warning')\n").warnings == ["my own warning"]


def test_callable_object_keeps_its_text_form():
    from r2py.stage4.comparators.data import DataComparator
    py = _run(SOUP).data["html"]
    r = {"__r2py_fp__": True, "class": ["xml_document", "xml_node"],
         "text": "<p>Hello <b>Hadley</b></p>"}
    res = DataComparator().compare({"html": r}, {"html": py})
    assert res.per_variable["html"] == 1.0, res.explanation


def test_function_still_compared_as_callable():
    py = _run("import functools\ndef f(a, b):\n    return a + b\ng = functools.partial(f, 1)\n").data["g"]
    assert py.get("__r2py_callable_meta__") and "value" not in py


def test_serializer_makes_no_warnings_even_when_all_are_shown():
    """The per-entity checkpoints serialize while the program runs, under the program's warning filters."""
    import warnings
    from bs4 import BeautifulSoup
    from r2py.stage0.effects.data import build_py_preamble
    ns = {}
    exec(build_py_preamble(), ns)
    soup = BeautifulSoup("<ul><li>1<li>2</ul>", "html.parser")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ns["_r2py_try_serialize"]("kids", list(soup.ul.children))
    assert [str(w.message) for w in caught] == []
