# pylint: disable=super-init-not-called

class RequiredPropertyException(Exception):

    def __init__(self, instance=None, message=None):
        self.instance = instance
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return f'The "{self.name}" property is a required field on "{self.instance}".'


class TransformNotCallableException(Exception):

    def __init__(self, instance=None, message=None):
        self.instance = instance
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return f'The "{self.name}" property\'s transform is not callable on "{self.instance}".'


class MetaclassNotSetException(Exception):

    def __init__(self, class_obj=None, message=None):
        self.class_obj = class_obj
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return f'The SDPropertyMetaclass was not set on "{self.class_obj}"' + \
               'The SDPropertyMetaclass metaclass must be the metaclass of ' + \
               'the highest class that uses an SDProperty:\n\nclass ' + \
               'ExampleClass(metaclass=SDPropertyMetaclass):\n\tpass\n\n' + \
               'class ExampleChildClass(ExampleClass):\n\tpass\n'


class MismatchedPropertyTypesException(Exception):

    def __init__(self, name, default, new_value, message=None):
        self.name = name
        self.default = default
        self.new_value = new_value
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return f"The '{self.name}' property's value and default are" + \
            f" of different types: '{self.default}' (type: " + \
            f"{type(self.default)}) != '{self.new_value}' " + \
            f"(type: {type(self.new_value)})"
