from tests.conftest import SuperkeyProperties


class TestSuperkeyProperties:

    def test_attribute_from_subkey(self):
        expected = 'sub_val'
        actual = SuperkeyProperties(subkey={'subkey_attr': 'sub_val'}).subkey_attr

        assert expected == actual

    def test_attribute_from_multi_deep_subkeys(self):
        expected = 'multi_sub_val'
        actual = SuperkeyProperties(subkey_1={'subkey_2': {'multi_subkey_attr': 'multi_sub_val'}}).multi_subkey_attr

        assert expected == actual
