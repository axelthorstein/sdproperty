from pytest import raises

from sdproperty.exceptions import RequiredPropertyException
from tests.conftest import RequiredProperties


class TestRequiredProperties:

    def test_required_attr_with_kwarg(self):
        expected = 'required_attr'
        actual = RequiredProperties(required_attr='required_attr').required_attr

        assert expected == actual

    def test_required_attr_with_no_kwarg_assigned(self):
        test_class = RequiredProperties()
        test_class.required_attr = 'new_attr'

        expected = 'new_attr'
        actual = test_class.required_attr

        assert expected == actual

    def test_defaulted_required_attr_with_no_kwarg(self):
        expected = 'defaulted_required_attr'
        actual = RequiredProperties().defaulted_required_attr

        assert expected == actual

    def test_defaulted_required_attr_with_kwarg(self):
        expected = 'new_required_attr'
        actual = RequiredProperties(defaulted_required_attr='new_required_attr').defaulted_required_attr

        assert expected == actual

    def test_required_attr_with_no_kwarg_raises_exception(self):
        with raises(RequiredPropertyException):
            RequiredProperties().required_attr
