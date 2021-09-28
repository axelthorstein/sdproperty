from tests.conftest import CallbackProperties


class TestCallbackProperties:

    def test_default_callback_is_called(self):
        expected = 'new_base_default'
        actual = CallbackProperties().get_callback_attr

        assert expected == actual

    def test_callback_is_called_owerwritten_by_kwarg(self):
        expected = 'get_callback_attr'
        actual = CallbackProperties(get_callback_attr='get_callback_attr').get_callback_attr

        assert expected == actual

    def test_callback_is_called_with_kwarg_dependency(self):
        expected = 'base_attr_callback'
        actual = CallbackProperties(base_attr='base_attr').get_callback_attr

        assert expected == actual
