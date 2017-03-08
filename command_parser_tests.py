import unittest
from command_parser import as_string_requested, extract_pv_name, uzhex_requested


class TestDecodingCommand(unittest.TestCase):

    def test_when_qualifiers_contains_dash_S_returns_as_string_equals_true(self):
        self.assertEqual(True, as_string_requested("caget -S -t IN:DEMO"))

    def test_when_qualifiers_does_not_contain_dash_S_returns_as_string_equals_false(self):
        self.assertEqual(False, as_string_requested("caget -t IN:DEMO"))

    def test_when_single_qualifier_is_dash_S_returns_as_string_equals_true(self):
        self.assertEqual(True, as_string_requested("caget -S IN:DEMO"))

    def test_when_qualifiers_contains_dash_S_returns_as_string_equals_true_despite_crazy_spacing(self):
        self.assertEqual(True, as_string_requested("caget  -S   -t    IN:DEMO"))

    def test_extract_pv_name_without_qualifiers_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", extract_pv_name("caget IN:DEMO:X:Y"))

    def test_extract_pv_name_with_qualifiers_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", extract_pv_name("caget -S -t IN:DEMO:X:Y"))

    def test_extract_pv_name_with_qualifiers_and_crazy_spacing_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", extract_pv_name("caget    -S     -t     IN:DEMO:X:Y   "))

    def test_extract_pv_name_with_qualifiers_and_uzhex_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", extract_pv_name("caget -S -t IN:DEMO:X:Y |uzhex"))

    def test_uzhex_requested_returns_true_when_present(self):
        self.assertEqual(True, uzhex_requested("caget -S -t IN:DEMO:X:Y |uzhex"))

    def test_uzhex_requested_returns_false_when_not_present(self):
        self.assertEqual(False, uzhex_requested("caget -S -t IN:DEMO:X:Y"))


if __name__ == '__main__':
    unittest.main()


