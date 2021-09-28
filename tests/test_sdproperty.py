from pytest import raises

from sdproperty.sdproperty import sdproperty
from sdproperty.sdproperty import SDProperty
from sdproperty.sdproperty import SDPropertyMetaclass

from tests.conftest import multiply


class SDPropertyTest(metaclass=SDPropertyMetaclass):

    base_attr               = SDProperty()
    default_attr            = SDProperty(default='default_attr')
    required_attr           = SDProperty(required=True)
    defaulted_required_attr = SDProperty(default='defaulted_required_attr', required=True)
    dependent_attr          = SDProperty(default=base_attr)
    updating_dependent_attr = SDProperty(default=base_attr, singleton=False)
    dict_combine_attr       = SDProperty(default={'key1': 'val1', 'key2': 'val2'})
    dict_overwrite_attr     = SDProperty(default={'key': 'val'}, combine_defaults=False)
    list_combine_attr       = SDProperty(default=['elem1'])
    list_overwrite_attr     = SDProperty(default=['elem1'], combine_defaults=False)
    subkey_attr             = SDProperty(superkeys=['superkey'])
    multi_subkey_attr       = SDProperty(superkeys=['superkey_1', 'superkey_2'])
    transform_attr          = SDProperty(transform=lambda x: x + 1)
    invalid_transform_attr  = SDProperty(transform='uncallable')
    transform_func_attr     = SDProperty(transform=multiply)
    transform_default_attr  = SDProperty(default=3, transform=multiply)
    get_callback_attr       = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @sdproperty
    def get_callback_attr(self):
        if not self.base_attr:
            return 'new_base_default'
        return self.base_attr + '_callback'


class TestSDProperty:

    def test_property_is_unset_on_descriptor(self):
        expected = True
        actual = SDProperty()._property_unset(SDPropertyTest(), 'unset_attr')

        assert expected == actual

    def test_property_is_set_on_descriptor(self):
        test_class = SDPropertyTest(base_attr='base_attr')
        test_class.base_attr

        expected = False
        actual = SDPropertyTest.base_attr._property_unset(test_class, 'base_attr')

        assert expected == actual

    def test_property_is_set_in_kwargs(self):
        test_class = SDPropertyTest(base_attr='base_attr')
        kwargs = SDPropertyTest.base_attr._get_instance_kwargs(test_class, None)

        expected = 'base_attr'
        actual = kwargs.get(SDPropertyTest.base_attr.name)

        assert expected == actual

    def test_property_is_set_in_subkey_kwargs(self):
        test_class = SDPropertyTest(superkey={'subkey_attr': 'sub_val'})
        kwargs = SDPropertyTest.subkey_attr._get_instance_kwargs(test_class, ['superkey'])

        expected = 'sub_val'
        actual = kwargs.get(SDPropertyTest.subkey_attr.name)

        assert expected == actual

    def test_property_is_set_in_multi_subkeys_deep_kwargs(self):
        test_class = SDPropertyTest(superkey_1={'superkey_2': {'multi_subkey_attr': 'multi_sub_val'}})
        kwargs = SDPropertyTest.multi_subkey_attr._get_instance_kwargs(test_class, ['superkey_1', 'superkey_2'])

        expected = 'multi_sub_val'
        actual = kwargs.get(SDPropertyTest.multi_subkey_attr.name)

        assert expected == actual

    def test_property_is_not_set_in_kwargs(self):
        test_class = SDPropertyTest()
        kwargs = SDPropertyTest.default_attr._get_instance_kwargs(test_class, None)

        expected = None
        actual = kwargs.get(SDPropertyTest.default_attr.name)

        assert expected == actual

    def test_required_property_is_not_set_and_not_defaulted(self):
        expected = True
        actual = SDPropertyTest.required_attr._required_value_not_set(None)

        assert expected == actual

    def test_required_property_is_not_set_but_defaulted(self):
        expected = False
        actual = SDPropertyTest.defaulted_required_attr._required_value_not_set('defaulted_required_attr')

        assert expected == actual

    def test_transform_value(self):
        test_class = SDPropertyTest()

        expected = 4
        actual = SDPropertyTest.transform_func_attr._apply_transform(2, test_class)

        assert expected == actual

    def test_valid_value(self):
        expected = None
        actual = SDPropertyTest.base_attr._value_is_valid(None)

        assert expected == actual

    def test_valid_value_with_default(self):
        expected = None
        actual = SDPropertyTest.default_attr._value_is_valid('default_attr')

        assert expected == actual

    def test_valid_value_with_callable_default(self):
        attribute = SDPropertyTest.transform_func_attr

        expected = None
        actual = attribute._value_is_valid(attribute.transform)

        assert expected == actual

    def test_valid_value_with_sdproperty_default(self):
        attribute = SDPropertyTest.dependent_attr

        expected = None
        actual = attribute._value_is_valid(attribute.default)

        assert expected == actual

    def test_default_is_not_cached_on_class_between_instances(self):
        test_class_1 = SDPropertyTest(base_attr='base_attr')

        test_class_1.dependent_attr
        test_class_1.base_attr = 'new_underlying_attr'
        test_class_1.dependent_attr

        test_class_2 = SDPropertyTest(base_attr='base_attr')
        test_class_2.base_attr = 'new_attr'

        expected = 'new_attr'
        actual = test_class_2.dependent_attr

        assert expected == actual
