from pytest import raises

from sdproperty.exceptions import InvalidPropertyException
from tests.conftest import ValidateProperties


class TestValidateProperties:

    def test_value_valid_regex(self):
        expected = 1
        actual = ValidateProperties(validate_regex_attr=1).validate_regex_attr

        assert expected == actual

    def test_value_invalid_regex_raises_exception(self):
        with raises(InvalidPropertyException):
            ValidateProperties(validate_regex_attr=0).validate_regex_attr

    def test_value_valid_lambda(self):
        expected = 1
        actual = ValidateProperties(validate_lambda_attr=1).validate_lambda_attr

        assert expected == actual

    def test_value_invalid_lamba_raises_exception(self):
        with raises(InvalidPropertyException):
            ValidateProperties(validate_lambda_attr=0).validate_lambda_attr

    def test_value_valid_func(self):
        expected = 'test'
        actual = ValidateProperties(validate_func_attr='test').validate_func_attr

        assert expected == actual

    def test_value_invalid_lamba_raises_exception(self):
        with raises(InvalidPropertyException):
            ValidateProperties(validate_func_attr=0).validate_func_attr
