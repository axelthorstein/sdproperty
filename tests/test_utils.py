from unittest import TestCase

from sdproperty.utils import combine_dicts
from sdproperty.utils import combine_lists
from sdproperty.utils import get_subkey_from_dict


class TestUtils(TestCase):

    def test_combine_dicts(self):
        # Tests that dictionary values passed in through d1 take precedence
        # over values in d2.
        expected = {'key1': 'val1', 'new_key': 'new_val', 'key2': 'updated_val'}
        actual = combine_dicts({
            'key1': 'val1',
            'key2': 'val2'
        }, {
            'new_key': 'new_val',
            'key2': 'updated_val'
        })

        assert expected == actual

    def test_combine_lists(self):
        expected = ['elem1', 'elem2']
        actual = combine_lists(['elem1'], ['elem1', 'elem2'])

        assert expected == actual

    def test_get_subkey_from_dict(self):
        expected = 'val1'
        actual = get_subkey_from_dict({
            'key1': 'val1',
            'key2': {'subkey1': 'subval1'}
        }, ['key1'])

        assert expected == actual

    def test_do_not_get_subkey_from_dict(self):
        expected = {'key1': 'val1'}
        actual = get_subkey_from_dict({'key1': 'val1'}, [])

        assert expected == actual

    def test_get_multi_subkeys_from_dict(self):
        expected = 'subval1'
        actual = get_subkey_from_dict({
            'key1': 'val1',
            'key2': {'subkey1': 'subval1'}
        }, ['key2', 'subkey1'])

        assert expected == actual
