from functools import wraps

from sdproperty.utils import combine_dicts
from sdproperty.utils import combine_lists
from sdproperty.utils import get_subkey_from_dict
from sdproperty.exceptions import MetaclassNotSetException
from sdproperty.exceptions import RequiredPropertyException
from sdproperty.exceptions import TransformNotCallableException
from sdproperty.exceptions import MismatchedPropertyTypesException


def sdproperty(func):
    """A decorator that simply adds a flag on to the function it's wrapping so
    that it can be identified later as being decorated by the sdproperty.
    """
    func.__sdproperty__ = True

    @wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)

    return decorator


class SDProperty:

    def __init__(self,
                 name=None,
                 default=None,
                 singleton=True,
                 required=False,
                 combine_defaults=True,
                 superkeys=None,
                 transform=None):
        self.name = name
        self.default = default
        self.singleton = singleton
        self.required = required
        self.combine_defaults = combine_defaults
        self.superkeys = superkeys
        self.transform = transform

    def _required_value_not_set(self, default):
        return default is None and self.required

    def _combine_with_defaults(self, value, default):
        if self.combine_defaults and default:
            if isinstance(value, dict):
                return combine_dicts(default, value)
            if isinstance(value, list):
                return combine_lists(default, value)

        return value

    def _apply_transform(self, value, instance):
        if self.transform:
            if callable(self.transform):
                return self.transform(value)
            raise TransformNotCallableException(self.name, instance)

        return value

    def _value_is_valid(self, value):
        if self.default and \
           not callable(self.default) and \
           not isinstance(self.default, SDProperty) and \
           not isinstance(value, type(self.default)):
            raise MismatchedPropertyTypesException(self.name, self.default, value)

    def _set_property_from_kwarg(self, instance, kwargs, default):
        # Set the attribute to the value passed into the kwarg.
        value = self._combine_with_defaults(kwargs[self.name], default)
        value = self._apply_transform(value, instance)
        self.__set__(instance, value)

    @staticmethod
    def _property_unset(instance, value):
        return instance.__dict__.get(value, None) is None

    @staticmethod
    def _verify_metaclass(class_object):
        if not isinstance(class_object, SDPropertyMetaclass):
            raise MetaclassNotSetException(class_object)

    @staticmethod
    def _get_instance_kwargs(instance, superkeys):
        if instance.__dict__.get('kwargs'):
            if superkeys:
                if isinstance(superkeys, SDProperty):
                    if not instance.__dict__.get(superkeys.name, None):
                        getattr(instance, superkeys.name)
                    return instance.__dict__[superkeys.name]
                else:
                    return get_subkey_from_dict(instance.kwargs, superkeys)
            return instance.kwargs
        return {}

    @staticmethod
    def _get_sdproperty_default(instance, default):
        if SDProperty._property_unset(instance, default.name):
            # If the default is another property, call it to get the value.
            return getattr(instance, default.name)

        # If default attr has already been evaluated, set to the stored value.
        return instance.__dict__[default.name]

    @staticmethod
    def _get_default(instance, default):
        # Note: We can't modify the class default attr so that it isn't cached.
        if isinstance(default, SDProperty):
            return SDProperty._get_sdproperty_default(instance, default)
        if callable(default):
            # If the default is a class method, evaluate and store the result.
            return default(instance)

        return default

    def __get__(self, instance, class_object):
        SDProperty._verify_metaclass(class_object)

        # Return if the property is called on an uninstantiated class.
        if instance is None:
            return self

        default = SDProperty._get_default(instance, self.default)
        instance_kwargs = SDProperty._get_instance_kwargs(instance, self.superkeys)

        if not self.singleton or SDProperty._property_unset(instance, self.name):
            # We have to check if not None in case the value is a negative bool.
            if self.singleton and instance_kwargs.get(self.name, None) is not None:
                self._set_property_from_kwarg(instance, instance_kwargs, default)
            elif self._required_value_not_set(default):
                raise RequiredPropertyException(self.name, instance)
            else:

                value = self._apply_transform(default, instance)
                self.__set__(instance, value)

        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self._value_is_valid(value)
        instance.__dict__[self.name] = value


class SDPropertyMetaclass(type):

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_val in attrs.items():
            if isinstance(attr_val, SDProperty):
                # Apply names to SDProperty descriptors.
                attr_val.name = attr_name
            elif hasattr(attr_val, '__sdproperty__'):
                attr_func = attr_val.__wrapped__
                # Replace the attribute with a SDProperty of the same name so
                # that when it's called it will evaluate the wrapped method.
                attrs[attr_name] = SDProperty(name=attr_name, default=attr_func)

        return super(SDPropertyMetaclass, cls).__new__(cls, name, bases, attrs)
