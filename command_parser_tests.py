import unittest
from command_parser import CaGetParser, AdGetParser


class TestDecodingCommand(unittest.TestCase):

    def test_caget_when_qualifiers_contains_dash_S_returns_as_string_equals_true(self):
        self.assertEqual(True, CaGetParser.as_string_requested("caget -S -t IN:DEMO"))

    def test_caget_when_qualifiers_does_not_contain_dash_S_returns_as_string_equals_false(self):
        self.assertEqual(False, CaGetParser.as_string_requested("caget -t IN:DEMO"))

    def test_caget_when_single_qualifier_is_dash_S_returns_as_string_equals_true(self):
        self.assertEqual(True, CaGetParser.as_string_requested("caget -S IN:DEMO"))

    def test_caget_when_qualifiers_contains_dash_S_returns_as_string_equals_true_despite_crazy_spacing(self):
        self.assertEqual(True, CaGetParser.as_string_requested("caget  -S   -t    IN:DEMO"))

    def test_caget_extract_pv_name_without_qualifiers_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", CaGetParser.extract_pv_name("caget IN:DEMO:X:Y"))

    def test_caget_extract_pv_name_with_qualifiers_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", CaGetParser.extract_pv_name("caget -S -t IN:DEMO:X:Y"))

    def test_caget_extract_pv_name_with_qualifiers_and_crazy_spacing_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", CaGetParser.extract_pv_name("caget    -S     -t     IN:DEMO:X:Y   "))

    def test_caget_extract_pv_name_with_qualifiers_and_uzhex_returns_name(self):
        self.assertEqual("IN:DEMO:X:Y", CaGetParser.extract_pv_name("caget -S -t IN:DEMO:X:Y |uzhex"))

    def test_caget_uzhex_requested_returns_true_when_present(self):
        self.assertEqual(True, CaGetParser.uzhex_requested("caget -S -t IN:DEMO:X:Y |uzhex"))

    def test_caget_uzhex_requested_returns_false_when_not_present(self):
        self.assertEqual(False, CaGetParser.uzhex_requested("caget -S -t IN:DEMO:X:Y"))

    def test_adget_pvprefix_extracted_correctly(self):
        self.assertEqual("13SIM1:image1", AdGetParser.extract_prefix("adget 13SIM1:image1"))

    def test_adget_pvprefix_extraction_removes_trailing_colon(self):
        self.assertEqual("13SIM1:image1", AdGetParser.extract_prefix("adget 13SIM1:image1:"))


if __name__ == '__main__':
    unittest.main()


