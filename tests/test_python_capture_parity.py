"""The Python capture serializes what the R capture serializes (2026-11-16).

R serializes a list element by element, so an xml2 nodeset is a list of node fingerprints, each with its text
(`as.character(node)`: the node alone, without the text after it). The Python capture fingerprinted only a whole
value: a list of lxml nodes became one fingerprint with no text (xml2 `kids` scored 0.25 for every program), and a
stdlib `xml.etree` element had no text form at all, so the comparator excluded it (threshold-095, xml2 b1).
R's values below are the stored ones (xml2 xml_attr's script map) or `as.character` printed by xml2 1.3."""
from r2py.types import EffectClass


def _fp(text):
    return {"__r2py_fp__": True, "class": ["xml_node"], "text": text}


R_KIDS = [_fp('<child id="a"/>'), _fp('<child id="b" d="b"/>')]
DOC = "x = ET.fromstring(\"<root id='1'><child id ='a' /><child id='b' d='b'/></root>\")\n"


def _run(src):
    from r2py.stage0.sandbox.isolation import TempWorkdir
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    with TempWorkdir() as wd:
        return PySandbox().run(src, workdir=wd, capture=frozenset({EffectClass.DATA}))


def _score(r, py_bundle, name="x"):
    from r2py.stage4.comparators.data import DataComparator
    return DataComparator().compare({name: r}, {name: py_bundle.data.get(name)}).per_variable.get(name)


def test_list_of_lxml_nodes_is_a_list_of_node_fingerprints():
    b = _run("import lxml.etree as ET\n" + DOC + "kids = list(x)\n")
    assert _score(R_KIDS, b, "kids") == 1.0


def test_stdlib_etree_element_has_xml2s_text_form():
    b = _run("import xml.etree.ElementTree as ET\n" + DOC + "kids = list(x)\n")
    assert _score(R_KIDS, b, "kids") == 1.0


def test_text_form_leaves_out_the_tail_as_xml2_does():
    src = "import lxml.etree as ET\nx = ET.fromstring('<r><a k=\"1\"/>tail<b>t</b></r>')\na = x[0]\n"
    assert _score(_fp('<a k="1"/>'), _run(src), "a") == 1.0


def test_wrong_node_still_fails():
    b = _run("import lxml.etree as ET\n" + DOC + "kids = list(x)[::-1]\n")
    assert _score(R_KIDS, b, "kids") < 0.5


def test_program_marker_still_refused_next_to_real_nodes():
    b = _run("import lxml.etree as ET\n" + DOC +
             "kids = [{'__r2py_fp__': True, 'class': ['xml_node'], 'text': '<child id=\"a\"/>'}, x[1]]\n")
    assert _score(R_KIDS, b, "kids") < 1.0


def test_plain_values_unchanged():
    b = _run("import datetime\nx = [1.5, 'a', None, {'k': [1, 2]}, datetime.date(2020, 1, 2)]\n")
    assert b.data["x"] == [1.5, "a", None, {"k": [1, 2]}, "2020-01-02"]
