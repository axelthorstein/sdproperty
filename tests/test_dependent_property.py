from tests.conftest import DependentProperties


class TestDependentProperties:

    def test_dependent_attr_has_base_attr_value(self):
        expected = 'base_attr'
        actual = DependentProperties(base_attr='base_attr').dependent_attr

        assert expected == actual

    def test_dependent_attr_has_its_own_value(self):
        expected = 'dependent_attr'
        actual = DependentProperties(base_attr='base_attr', dependent_attr='dependent_attr').dependent_attr

        assert expected == actual

    def test_dependent_attr_overwritten_on_assignment(self):
        test_class = DependentProperties(base_attr='base_attr')

        expected = 'base_attr'
        actual = test_class.dependent_attr

        assert expected == actual

        test_class.dependent_attr = 'dependent_attr'

        expected = 'dependent_attr'
        actual = test_class.dependent_attr

        assert expected == actual

    def test_dependent_attr_is_not_changed_when_underlying_attr_changes_after(self):
        test_class = DependentProperties(base_attr='base_attr')

        expected = 'base_attr'
        actual = test_class.dependent_attr

        assert expected == actual

        test_class.base_attr = 'new_underlying_attr'

        expected = 'base_attr'
        actual = test_class.dependent_attr

        assert expected == actual

    def test_dependent_attr_is_changed_when_underlying_attr_changes_before(self):
        test_class = DependentProperties(base_attr='base_attr')
        test_class.base_attr = 'new_attr'

        expected = 'new_attr'
        actual = test_class.dependent_attr

        assert expected == actual

    def test_dependent_attr_is_updated_with_depended_on_attr(self):
        test_class = DependentProperties(base_attr='base_attr')

        test_class.updating_dependent_attr
        test_class.base_attr = 'new_underlying_attr'

        expected = 'new_underlying_attr'
        actual = test_class.updating_dependent_attr

        assert expected == actual

    def test_attr_is_dependent_on_another_sdproperty(self):
        config = {'base_attr': {'sdproperty_dependent_attr': 'test'}}
        test_class = DependentProperties(**config)

        expected = 'test'
        actual = test_class.sdproperty_dependent_attr

        assert expected == actual

    def test_attr_is_dependent_on_nested_sdproperty(self):
        config = {'parent_1': {'parent_2': {'nested_parent_attr': {'nested_dependent_attr': 'val'}}}}
        test_class = DependentProperties(**config)

        expected = 'val'
        actual = test_class.nested_dependent_attr

        assert expected == actual
