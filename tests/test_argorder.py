"""Token-based argument reordering: fixes the R-style call, leaves everything else alone."""
import ast
import unittest

from r2py.stage2.argorder import repair_argument_order as fix


class TestFixes(unittest.TestCase):
    def check(self, src, want, n=1):
        out, k = fix(src)
        self.assertEqual((out, k), (want, n))
        ast.parse(out)

    def test_the_translators_usual_mistake(self):
        self.check("g(data=df, aes('x', 'y'), fill='g', alpha=0.3)\n",
                   "g(aes('x', 'y'), data=df, fill='g', alpha=0.3)\n")

    def test_several_positionals_keep_their_order_and_star_args_stay_with_them(self):
        self.check("f(a=1, x, *rest, b=2, y, **kw)\n", "f(x, *rest, y, a=1, b=2, **kw)\n")

    def test_nested_and_multiline_calls(self):
        src = "p = (ggplot(d)\n     + geom(data=d, aes('x'), size=2)\n     + theme(k=1, v(m=1, 2)))\n"
        out, k = fix(src)
        self.assertEqual(k, 3)  # geom, v, and theme (whose positional v(...) follows k=1)
        ast.parse(out)
        self.assertIn("geom(aes('x'), data=d, size=2)", out)
        self.assertIn("theme(v(2, m=1), k=1)", out)

    def test_string_with_commas_and_equals_is_one_argument(self):
        self.check("f(k=1, 'a, b=c', g(z, w=2))\n", "f('a, b=c', g(z, w=2), k=1)\n")

    def test_trailing_comma_is_tolerated(self):
        out, k = fix("f(k=1, x,)\n")
        self.assertEqual(k, 1)
        ast.parse(out)


class TestLeavesAlone(unittest.TestCase):
    def test_valid_code_is_returned_unchanged(self):
        src = ("def f(a, b=1, *c, d=2, **e):\n    return (a, b, [1, 2], {'k': 1}, x[1:2])\n"
               "class A(B, metaclass=M): pass\nf(1, b=2)\nf(*a, k=1)\nf(**kw)\nprint(f'{a=}', end='')\n"
               "lambda x=1: x\nz = dict(a=1, b=2)\nif (a == b): pass\n")
        self.assertEqual(fix(src), (src, 0))

    def test_tuples_subscripts_and_defs_are_not_calls(self):
        src = "x = (k, 1)\ny = d[k=1] if False else 0\n"
        self.assertEqual(fix(src)[1], 0)
        self.assertEqual(fix("def f(a=1, b):\n    pass\n")[1], 0)   # a different error; not ours

    def test_a_call_with_a_comment_inside_is_skipped(self):
        src = "f(k=1,\n  # r2py:entity:e1\n  x)\n"
        self.assertEqual(fix(src), (src, 0))

    def test_untokenisable_source_is_returned_as_is(self):
        self.assertEqual(fix("f(k=1, x\n"), ("f(k=1, x\n", 0))


if __name__ == "__main__":
    unittest.main()
