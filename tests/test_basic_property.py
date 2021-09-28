from tests.conftest import BasicProperties


class TestBasicProperties:

    def test_base_attr_is_none(self):
        expected = None
        actual = BasicProperties().base_attr

        assert expected == actual

    def test_base_attr_is_overwritten_by_kwarg(self):
        expected = 'new_attr'
        actual = BasicProperties(base_attr='new_attr').base_attr

        assert expected == actual

    def test_base_attr_is_overwritten_by_assignment(self):
        test_class = BasicProperties()
        test_class.base_attr = 'new_attr'

        expected = 'new_attr'
        actual = test_class.base_attr

        assert expected == actual

    def test_base_attr_is_overwritten_when_set_explicitly(self):
        test_class = BasicProperties(base_attr='new_attr')

        expected = 'new_attr'
        actual = test_class.base_attr

        assert expected == actual

        test_class.base_attr = 'explicitly_set_attr'

        expected = 'explicitly_set_attr'
        actual = test_class.base_attr

        assert expected == actual
