from pytest import raises

from sdproperty.exceptions import MetaclassNotSetException
from tests.conftest import NoMetaclass


class TestNoMetaclass:

    def test_metaclass_is_set_on_class_raises_exception(self):
        with raises(MetaclassNotSetException):
            NoMetaclass().base_attr
