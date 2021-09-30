### SDProperty

#### SDProperty AKA Singleton, Defaulted Property.

----------------

#### TL;DR

The `SDProperty` is a custom class that extends the functionality of Pythons `@property` decorator. It works much in the same way, however it allows you to set defaults for properties if they aren't passed in, they aren't reevaluated every time they're accessed, they can depend on each other, or it can be used as a decorator with `@sdproperty`. The syntax is simple:
```python
class Example(metaclass=SDPropertyMetaclass):
    basic_property = SDProperty(default='base')

    def __init__(self, **kwargs):
        self.kwargs = kwargs

>>> Example().basic_property
'base'
```

This is the basic idea. All of the options and semantics will be explained below.

#### Motivation:

Let's say you need a factory class that takes in a large number of configurations, or you expect the configurations to grow over time to the point where it may become unmanageable. Perhaps each of these configurations may need a default value if it isn't supplied. You can handle this in a number of ways. One way is that you could pass each field into the class as a defaulted keyword argument, then assign each keyword into a class attribute in the `__init__` method, and then store it as a property so that it isn't recalculated when it's accessed. Another way would be passing in a configuration dictionary and parsing out all the values you need. This would require some way of also keeping track of each configurations' default value, and likely setting some, or all, as properties. Either way you would probably want some variation on:

- Validation on some of the attributes and not others.
- Heavy computation on some attributes.
- Some external call when an attribute is set or accessed for the first time (eg. sending a metric or making a web request).
- Some dictionary arguments to be _conbined_ with the defaults you've set (where the keyword arguments' values take precedence over the default values), and others to be overwritten. 
- Some list arguments appended to defaults and others overwritten.

At this point, in order to achieve this, for each configuration option you have a keyword argument with(out) a default value, an attribute assignment in the initialization method, and a property function for every field in your configuration that potentially makes the property a singleton. At this point, chances are that your class is bloated and contains a lot more configuration parsing code than actual logic.

This is where an `SDProperty` would be useful. Using an `SDProperty` you can set a default, verify that it's passed in as a keyword argument, access it like a property (and therefore avoid recalculation), have it depend on other `SDProperties`, and have it lazy load so that if it's not accessed it won't be evaluated in the first place. All of this, potentially in a single line. This way you can turn something like this:

```python
class ExampleClass():

    def __init__(self,
                 base_attr,
                 defaulted_attr='example_default',
                 validated_attr=None,
                 dict_combine_attr={},
                 dict_overwrite_attr={'key': 'val'},
                 list_combine_attr=['elem1'],
                 list_overwrite_attr=['elem1']):
        self.base_attr = base_attr
        self.defaulted_attr = defaulted_attr
        self.validated_attr = validated_attr
        self.dict_combine_attr = dict_combine_attr
        self.dict_overwrite_attr = dict_overwrite_attr
        self.list_combine_attr = list_combine_attr
        self.list_overwrite_attr = list_overwrite_attr

    @property
    def base_attr(self):
        if not self.base_attr:
            raise Exception('base_attr cannot be empty ({}, [], "")')
        return self.base_attr

    @property
    def defaulted_attr(self):
        return self.defaulted_attr

    @property
    def validated_attr(self):
        if 0 < len(self.validated_attr) < 64:
            return self.validated_attr
        raise Exception("Value is not the correct length.")

    @property
    def dict_combine_attr(self):
        defaults = ={'key1': 'val1', 'key2': 'val2'}
        new_dict_combine_attr = self.dict_combine_attr.copy()
        new_dict_combine_attr.update(defaults)
        return new_dict_combine_attr

    @property
    def dict_overwrite_attr(self):
        return self.dict_overwrite_attr

    @property
    def list_combine_attr(self):
        defaults = ['elem2']
        return defaults + self.list_combine_attr

    @property
    def list_overwrite_attr(self):
        return self.list_overwrite_attr

```

into this:

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr           = SDProperty()
    defaulted_attr      = SDProperty(default='example_default')
    validated_attr      = SDProperty(validate=lambda x: 0 < x < 64)
    dict_combine_attr   = SDProperty(default={'key1': 'val1', 'key2': 'val2'})
    dict_overwrite_attr = SDProperty(default={'key': 'val'}, combine_defaults=False)
    list_combine_attr   = SDProperty(default=['elem1'], combine_defaults=True)
    list_overwrite_attr = SDProperty(default=['elem1'])

    def __init__(self, **kwargs):
        self.kwargs = kwargs

```

Then, if there is a property that has more complicated default logic, or another method needs to be executed when the property is set, then a regular property can be written using the accompanying decorator:

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @sdproperty
    def callback_attr(self):
        self.make_external_call()

        if not self.base_attr:
            return 'new_base_default'

        return 'callback_attr'

```
The `callback_attr` attribute can be evaluated just like an `SDProperty`, except when it's accessed it will execute the function. It will only evaluate the first time it's accessed and it's able to base it's return on another attribute.


#### Notes:

##### Setting the `kwargs` Attribute:

`SDProperties` will check if a key of the same name is set in the `kwargs` attribute on the class. For example:
```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs

>>> ExampleClass(base_attr='new_attr').base_attr
'new_attr'
```
Here the value of the `base_attr` property is set because a keyword argument of the same name is passed into the class instantiation. So, in order for this to be possible, it is assumed that:

```python
def __init__(self, *args, **kwargs):
    self.kwargs = kwargs
```

is set when the class is instantiated. However, if the `kwargs` attribute is not set the property will still work, but with limited functionality. You’ll be able to set properties with defaults, set those properties explicitly with assignments after the class is instantiated (in the format `my_instance.myattr = 'explicitly_set'`), and they’ll be accessible in the class, but you won’t be able to pass `kwargs` into the class. An example of using it without setting `self.kwargs` would be (it's always recommended that you just set `self.kwargs`):
```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr = SDProperty()

    def __init__(self, unrelated_example_kwarg):
        self.unrelated_example_kwarg = unrelated_example_kwarg


>>> example_class = ExampleClass(base_attr='new_attr')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() got an unexpected keyword argument 'base_attr'
>>> example_class = ExampleClass(base_attr='new_attr')

```


##### Class Attributes and Methods

If an SD property is set on the class and then redefined as a class method that is decorated with the `sdproperty` decorator, the initial definition will be overwritten by the class method and never executed (and therefore the default is ignored):

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    example_property = SDProperty(default='example_default')
    
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    @sdproperty
    def example_property(self):
        return 'overwritten_example_default'


>>> ExampleClass().example_property
'overwritten_example_default'
```


##### SDPropertyMetaclass

The `SDPropertyMetaclass` must be set on any class that uses an `SDProperty`, otherwise the properties won't have their names set and won't be able to function properly.


##### Class Inheritance

If a property is set on a child class it will overwrite the default value or implementation of an `SDProperty` on a parent class:

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr = SDProperty(default='base_attr')

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class ExampleChildClass(ExampleClass):
    base_attr = SDProperty(default='new_base_attr')


>>> ExampleClass().base_attr
'base_attr'
>>> ExampleChildClass().base_attr
'new_base_attr'
```


##### Dependent Properties

If one property needs to depend on the value of another, this is possible by passing the property of the depended on attribute as the default of the dependent attribute:

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr      = SDProperty(default='base_attr')
    dependent_attr = SDProperty(default=base_attr)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


>>> example_class = ExampleClass()
>>> example_class.dependent_attr
'base_attr'
```

Notice how the `base_attr` hadn't been initialized, but the accessing of the `dependent_attr` in turn called `base_attr` to get it's value.

If the `base_attr` is then updated however, this will not be reflected in the `dependent_attr`, unless it occurs before the `dependent_attr` is called:

```python
>>> example_class = ExampleClass()
>>> example_class.dependent_attr
'base_attr'
>>> example_class.base_attr = 'new_attr'
>>> example_class.dependent_attr # The dependent attribute hasn't changed.
'base_attr'
```

```python
>>> example_class = ExampleClass()
>>> example_class.base_attr = 'new_attr'
>>> example_class.dependent_attr # The dependent attribute has the new base attribute value, not the default.
'new_attr'
```
Here it takes the assigned value of the `base_attr`, because it's already been stored on the instance.

If this process is repeated however, the value will not change because the dependent attribute is already stored on the instance and will be retrieved instead of recalculated:
```python
>>> example_class = ExampleClass()
>>> example_class.base_attr = 'new_attr'
>>> example_class.dependent_attr
'new_attr'
>>> example_class.base_attr = 'second_new_attr'
>>> example_class.dependent_attr
'new_attr'
```

If you want a dependent property to get the updated value of the property that it depends on, you can set the `singleton` argument to `False`:
```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr      = SDProperty(default='base_attr')
    dependent_attr = SDProperty(default=base_attr, singleton=False)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


>>> example_class = ExampleClass()
>>> example_class.base_attr = 'new_attr'
>>> example_class.dependent_attr
'new_attr'
>>> example_class.base_attr = 'second_new_attr'
>>> example_class.dependent_attr
'second_new_attr'
```

If you have a configuration that has a lot of nested configs and you don't want to explicity set out the list of super keys for each property you can create a property for a single parent and then base other properties off of that property. For example:
```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    parent_attr    = SDProperty()
    dependent_attr = SDProperty(superkeys=parent_attr)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

>>> config = {'parent_attr': {'dependent_attr': 'val'}}
>>> example_class = ExampleClass()
>>> example_class.dependent_attr
'val'
```

##### Dependent Properties + Class Inheritance

If we use the same example from the `Class Inheritance` section, but change the child property to be dependent on a property in the parent class it would look like this:

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    base_attr = SDProperty(default='base_attr')

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class ExampleChildClass(ExampleClass):
    dependent_attr = SDProperty(default=ExampleClass.base_attr)


>>> ExampleChildClass().dependent_attr
'base_attr'
```

Notice here that in order to depend on a property from the parent class it must be prefixed by the class name.


#### Basing a Property on Subkeys in `kwargs`

If you need to pass in dictionaries with multiple levels, but still want to map a property to a key in the dictionary you can use the `superkeys` keyword to define which super keys to look into to find the property:

```python
class ExampleClass(metaclass=SDPropertyMetaclass):
    subkey_attr = SDProperty(superkeys=('parent_1', 'parent_2'))

    def __init__(self, **kwargs):
        self.kwargs = kwargs

>>> config = {'parent_1': {'parent_2': {'sub_attr': 'sub_val'}}}
>>> example_class = ExampleClass(**config)
>>> example_class.subkey_attr
'sub_val'
```

Note that the first subkey is the name of the keyword in `kwargs`, then each subsequent subkey is the name of a key. Using this strategy you could potentially store all of your configs as a multi level JSON blob and pass them directly into the class.


#### Validating Properties

In the case that some validation needs to be done on a property there is the `validate` keyword. Validation can come in the form of a regex pattern, a simple lamdba function, or a traditional function.

```Python
class ExampleClass(metaclass=SDPropertyMetaclass):

    def validate_str(string):
        if isinstance(string, str):
            return True

    validate_regex_attr  = SDProperty(validate='^[1-9]?$|^64$')
    validate_lambda_attr = SDProperty(validate=lambda x: 0 < x < 2)
    validate_func_attr   = SDProperty(validate=validate_str)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

>>> example_class = ExampleClass(validate_regex_attr=1).validate_regex_attr
1
>>> ExampleClass(validate_regex_attr=0)
# raises InvalidPropertyException
```
Note: If validation is done by a traditional function it either needs to be defined outside of the class or above the properties in the class. At the time of evaluation the class isn't instantiated yet so you cannot validate properties with class methods.


#### The Transform Keyword

If a property needs minor transformations after it's pulled out of the keyword arguments you can use the `transform` keyword:

```python
def multiply(value):
    return value * 2


class ExampleClass(metaclass=SDPropertyMetaclass):
    lambda_transform_attr    = SDProperty(transform=lambda x: x + 1)
    defaulted_transform_attr = SDProperty(default=2, transform=lambda x: x + 1)
    function_transform_attr  = SDProperty(transform=multiply)

    def __init__(self, **kwargs):
        self.kwargs = kwargs


>>> example_class = ExampleClass(lambda_transform_attr=1, function_transform_attr=2)
>>> example_class.lambda_transform_attr
2
>>> example_class.defaulted_transform_attr
3
>>> example_class.function_transform_attr
4
```

Notice that if you are defining a function to be passed to transform it must only take a single argument (`value`), as that will be the attribute taken from the keyword arguments. Also, if you define a default (and it isn't overwritten by keyword argument) it will also be transformed.

If, in your function, you plan on doing transformations based on other class methods or attributes then you should use the `sdproperty` decorator on a regular class method instead. You will find documentation about the decorator above. If you try to reference another attribute in the `lambda` transform method of an attribute, it won't be in the correct scope to access it and therefore won't work.


### TODO:

- Add sets combination.


-------

Inspired in part by [this article on descriptors and metaclasses](https://nbviewer.jupyter.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb).
