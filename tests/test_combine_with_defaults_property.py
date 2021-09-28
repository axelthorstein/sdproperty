from tests.conftest import CombineWithDefaultsProperties


class TestCombineWithDefaultsProperties:

    def test_dict_attr_is_combined_with_defaults(self):
        # Tests that dictionary values passed in through a kwarg takes precedence
        # over values in the defaults dictionary.
        expected = {'key1': 'val1', 'new_key': 'new_val', 'key2': 'updated_val'}
        actual = CombineWithDefaultsProperties(dict_combine_attr={'new_key': 'new_val', 'key2': 'updated_val'}).dict_combine_attr

        assert expected == actual

    def test_dict_attr_is_not_combined_with_defaults(self):
        expected = {'new_key': 'new_val'}
        actual = CombineWithDefaultsProperties(dict_overwrite_attr={'new_key': 'new_val'}).dict_overwrite_attr

        assert expected == actual

    def test_dict_attr_on_multiple_instances_is_not_cached(self):
        test_class_1 = CombineWithDefaultsProperties()
        assert {'key': 'val'} == test_class_1.dict_overwrite_attr

        test_class_1.dict_overwrite_attr = {'new_key': 'new_val'}
        assert {'new_key': 'new_val'} == test_class_1.dict_overwrite_attr

        test_class_2 = CombineWithDefaultsProperties()
        assert {'key': 'val'} == test_class_2.dict_overwrite_attr

    def test_list_attr_is_combined_with_defaults(self):
        expected = ['elem1', 'elem2']
        actual = CombineWithDefaultsProperties(list_combine_attr=['elem2']).list_combine_attr

        assert expected == actual

    def test_list_attr_is_not_combined_with_defaults(self):
        expected = ['elem2']
        actual = CombineWithDefaultsProperties(list_overwrite_attr=['elem2']).list_overwrite_attr

        assert expected == actual

    def test_list_attr_is_combined_with_existing_val_on_explicit_setting(self):
        test_class = CombineWithDefaultsProperties()
        test_class.list_overwrite_attr += ['elem2']

        expected = ['elem1', 'elem2']
        actual = CombineWithDefaultsProperties().list_overwrite_attr

        assert expected == actual

    def test_resetting_attribute_overwrites_always(self):
        test_class = CombineWithDefaultsProperties(dict_combine_attr={'new_key': 'new_val', 'key2': 'updated_val'})

        expected = {'key1': 'val1', 'new_key': 'new_val', 'key2': 'updated_val'}
        actual = test_class.dict_combine_attr

        assert expected == actual

        test_class.dict_combine_attr = {'overwritten_key': 'overwritten_val'}

        expected = {'overwritten_key': 'overwritten_val'}
        actual = test_class.dict_combine_attr

        assert expected == actual
