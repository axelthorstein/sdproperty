from pytest import raises

from sdproperty.exceptions import TransformNotCallableException
from tests.conftest import TransformProperties


class TestTransformSDProperty:

    def test_attribute_is_transformed_by_lambda(self):
        expected = 2
        actual = TransformProperties(transform_attr=1).transform_attr

        assert expected == actual

    def test_attribute_is_transformed_by_function(self):
        expected = 4
        actual = TransformProperties(transform_func_attr=2).transform_func_attr

        assert expected == actual

    def test_attribute_is_transformed_by_function_with_default(self):
        expected = 6
        actual = TransformProperties().transform_default_attr

        assert expected == actual

    def test_attribute_is_transformed_raises_exception(self):
        with raises(TransformNotCallableException):
            TransformProperties().invalid_transform_attr
