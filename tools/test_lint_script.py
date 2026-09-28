"""Offline regressions for the static VDJScript linter: one case per rule, plus the
vendor forms that once raised false errors."""
import unittest

from lint_script import Vocabulary, lint_script, xml_scripts

VOCAB = Vocabulary()


def rules(script, context="action"):
    return {(f.level, f.rule) for f in lint_script(script, context, VOCAB)}


class RuleTests(unittest.TestCase):
    def test_clean_scripts_raise_nothing(self):
        for script in ("set '$mode' 1 & play ? loop 4 : nothing",
                       "var_equal '$mode' 1 ? do_one : var_equal '$mode' 2 ? play : pause",
                       "deck left effect_active 1 ? blink 500ms : off",
                       "beatjump +4", "beatjump -0.5"):
            self.assertEqual(rules(script) - {("warning", "unknown-verb")}, set(), script)

    def test_errors(self):
        self.assertIn(("error", "unterminated"), rules("effect_stems 'rhythm''"))
        self.assertIn(("error", "unterminated"), rules("play `get_bpm"))
        self.assertIn(("error", "parens"), rules("( wait 1000ms & play"))
        self.assertIn(("error", "empty-branch"), rules("shift ? loop 32 ? : off"))
        self.assertIn(("error", "empty-branch"), rules("shift ? play : "))
        self.assertIn(("error", "disproved"), rules("browser_search 'x'"))

    def test_warnings(self):
        cases = {
            "unknown-verb": "lopp_roll 4",
            "and-guard": "var_equal '$x' 1 && play",
            "and-condition": "loaded && play ? blink : off",
            "beatjump-unsigned": "beatjump 4",
            "computed-arg": "loop `get_var '$n'`",
            "sampler-loaded-auto": "sampler_loaded 8 'auto' ? on : off",
            "string-variable": "set '$mode' 'reverb'",
            "truthiness-trap": "get_bpm ? play : pause",
            "literal-branch": "on ? 'A' : 'B'",
            "comment": "play // pause",
            "deck-target": "deck qqqq play",
        }
        for rule, script in cases.items():
            self.assertIn(("warning", rule), rules(script), script)

    def test_notes(self):
        self.assertIn(("note", "trailing-chain"), rules("loaded ? play : pause & stop"))
        self.assertIn(("note", "truthiness-trap"), rules("effect_select ? on : off"))
        self.assertIn(("note", "query-selector"), rules("filter_selectcolorfx 'Echo'", "query"))

    def test_and_is_fine_as_a_query_value(self):
        self.assertNotIn(("warning", "and-guard"), rules("loaded && play", "query"))

    def test_vendor_forms_that_are_not_errors(self):
        # A quote holding a backtick segment that holds quotes.
        self.assertEqual({r for r in rules("param_equal '`pitch_slider`' '`pitch`' ? color 'white' : color 'red'")
                          if r[0] == "error"}, set())
        # A parenthesised branch is not an empty one.
        self.assertEqual({r for r in rules("setting 'x' ? (loaded ? constant 1 : constant 3) : (constant 0)")
                          if r[0] == "error"}, set())
        # Wrapper sub-keywords and skin placeholders are not verbs.
        for script in ("effect slider 3 50%", "sampler 2 play", "get position", "[ACTION] ? blink", "deck [LEFTDECK] play"):
            self.assertEqual(rules(script), set(), script)

    def test_backticks_are_linted_as_queries(self):
        self.assertIn(("error", "empty-branch"), rules("set '$v' `loaded ? :`"))


class XmlTests(unittest.TestCase):
    def test_extraction_contexts_and_lines(self):
        text = ('<page name="p">\n'
                '<pad1 name="`get_bpm`" query="loaded &amp;&amp; play">play &amp; stop</pad1>\n'
                '</page>')
        found = {(line, attr, context, script) for line, attr, context, script in xml_scripts(text)}
        self.assertIn((2, "query", "query", "loaded && play"), found)
        self.assertIn((2, "name", "query", "`get_bpm`"), found)
        self.assertIn((2, "<pad1>", "action", "play & stop"), found)


if __name__ == "__main__":
    unittest.main()
