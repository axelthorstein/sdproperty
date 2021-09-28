from tests.conftest import InheritedDefaultedProperties
from tests.conftest import InheritedDependentProperties
from tests.conftest import InheritedCallbackProperties


class TestInheritedProperties:

    def test_default_attr_overwritten_by_child_default(self):
        expected = 'child_default'
        actual = InheritedDefaultedProperties().default_attr

        assert expected == actual

    def test_default_attr_overwritten_by_child_kwarg(self):
        expected = 'kwarg_val'
        actual = InheritedDefaultedProperties(default_attr='kwarg_val').default_attr

        assert expected == actual

    def test_dependent_attr_in_child(self):
        expected = 'base_attr'
        actual = InheritedDependentProperties(base_attr='base_attr').child_dependent_attr

        assert expected == actual

    def test_callback_is_called_from_child(self):
        expected = 'new_child_base_default'
        actual = InheritedCallbackProperties().get_callback_attr

        assert expected == actual

    def test_callback_is_called_from_child_with_kwarg_dependency(self):
        expected = 'base_attr_child_callback'
        actual = InheritedCallbackProperties(base_attr='base_attr').get_callback_attr

        assert expected == actual
