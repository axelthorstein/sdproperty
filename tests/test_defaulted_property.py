from pytest import raises

from sdproperty.exceptions import MismatchedPropertyTypesException
from tests.conftest import DefaultedProperties


class TestDefaultedProperties:

    def test_default_attr(self):
        expected = 'default_attr'
        actual = DefaultedProperties().default_attr

        assert expected == actual

    def test_default_attr_is_overwritten_by_kwarg(self):
        expected = 'new_attr'
        actual = DefaultedProperties(default_attr='new_attr').default_attr

        assert expected == actual

    def test_default_attr_is_overwritten_by_assignment(self):
        test_class = DefaultedProperties()
        test_class.default_attr = 'new_attr'

        expected = 'new_attr'
        actual = test_class.default_attr

        assert expected == actual

    def test_mismatched_default_and_kwarg_types_raises_exception(self):
        with raises(MismatchedPropertyTypesException):
            DefaultedProperties(default_attr=1).default_attr

    def test_invalid_value_mismatched_types_raises_exception(self):
        with raises(MismatchedPropertyTypesException):
            DefaultedProperties.default_attr._value_is_valid(1)
