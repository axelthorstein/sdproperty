from sdproperty.sdproperty import sdproperty
from sdproperty.sdproperty import SDProperty
from sdproperty.sdproperty import SDPropertyMetaclass


def multiply(value):
    return value * 2


class BasicProperties(metaclass=SDPropertyMetaclass):
    base_attr = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class DefaultedProperties(metaclass=SDPropertyMetaclass):
    default_attr = SDProperty(default='default_attr')

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class RequiredProperties(metaclass=SDPropertyMetaclass):
    required_attr = SDProperty(required=True)
    defaulted_required_attr = SDProperty(default='defaulted_required_attr', required=True)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class DependentProperties(metaclass=SDPropertyMetaclass):
    base_attr                 = SDProperty()
    dependent_attr            = SDProperty(default=base_attr)
    updating_dependent_attr   = SDProperty(default=base_attr, singleton=False)
    sdproperty_dependent_attr = SDProperty(superkeys=base_attr)
    nested_parent_attr        = SDProperty(superkeys=['parent_1', 'parent_2'])
    nested_dependent_attr     = SDProperty(superkeys=nested_parent_attr)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class CombineWithDefaultsProperties(metaclass=SDPropertyMetaclass):
    dict_combine_attr   = SDProperty(default={'key1': 'val1', 'key2': 'val2'})
    dict_overwrite_attr = SDProperty(default={'key': 'val'}, combine_defaults=False)
    list_combine_attr   = SDProperty(default=['elem1'])
    list_overwrite_attr = SDProperty(default=['elem1'], combine_defaults=False)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class TransformProperties(metaclass=SDPropertyMetaclass):
    transform_attr         = SDProperty(transform=lambda x: x + 1)
    invalid_transform_attr = SDProperty(transform='uncallable')
    transform_func_attr    = SDProperty(transform=multiply)
    transform_default_attr = SDProperty(default=3, transform=multiply)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class CallbackProperties(metaclass=SDPropertyMetaclass):
    base_attr         = SDProperty()
    get_callback_attr = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @sdproperty
    def get_callback_attr(self):
        if not self.base_attr:
            return 'new_base_default'
        return self.base_attr + '_callback'


class InheritedDefaultedProperties(DefaultedProperties):
    default_attr = SDProperty(default='child_default')


class InheritedDependentProperties(DependentProperties):
    child_dependent_attr = SDProperty(default=DependentProperties.dependent_attr)


class InheritedCallbackProperties(CallbackProperties):

    @sdproperty
    def get_callback_attr(self):
        if not self.base_attr:
            return 'new_child_base_default'
        return self.base_attr + '_child_callback'


class SuperkeyProperties(metaclass=SDPropertyMetaclass):
    subkey_attr       = SDProperty(superkeys=['subkey'])
    multi_subkey_attr = SDProperty(superkeys=['subkey_1', 'subkey_2'])

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class NoMetaclass():
    base_attr = SDProperty()
