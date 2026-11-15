"""A program cannot forge the harness's fingerprint format (2026-11-15).

The capture writes ``{'__r2py_fp__': True, ...}`` only for an object JSON cannot represent. A program that builds such
dicts itself (xml2 ``kids`` as ``{'__r2py_fp__': True, 'class': ['xml_node'], 'text': ...}``, seen in threshold-095
and in finals of the default) had them compared as R's node fingerprints and passed on text it merely copied."""
from r2py.types import EffectClass

R_NODE = {"__r2py_fp__": True, "class": ["xml_node"], "text": "<b>t</b>"}


def _run(src):
    from r2py.stage0.sandbox.isolation import TempWorkdir
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    with TempWorkdir() as wd:
        return PySandbox().run(src, workdir=wd, capture=frozenset({EffectClass.DATA}))


def _score(r, py):
    from r2py.stage4.comparators.data import DataComparator
    return DataComparator().compare({"x": r}, {"x": py}).per_variable["x"]


def test_forged_dict_is_not_a_fingerprint():
    py = _run("x = [{'__r2py_fp__': True, 'class': ['xml_node'], 'text': '<b>t</b>'}]\n").data["x"]
    assert _score([R_NODE], py) == 0.0


def test_forged_dict_subclass_is_not_a_fingerprint():
    src = ("class XmlNode(dict):\n    pass\n"
           "x = XmlNode({'__r2py_fp__': True, 'class': ['xml_node'], 'text': '<b>t</b>'})\n")
    assert _score(R_NODE, _run(src).data["x"]) == 0.0


def test_real_object_still_matches():
    src = "from lxml import etree\nx = etree.fromstring('<b>t</b>')\n"
    assert _score(R_NODE, _run(src).data["x"]) == 1.0
