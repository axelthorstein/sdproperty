import yaml

from sdproperty.sdproperty import sdproperty
from sdproperty.sdproperty import SDProperty
from sdproperty.sdproperty import SDPropertyMetaclass


class Person(metaclass=SDPropertyMetaclass):

    email = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Name(metaclass=SDPropertyMetaclass):

    first = SDProperty()
    last  = SDProperty()

    def __init__(self, **kwargs):
        self.kwargs = kwargs


config = yaml.safe_load("""
name: 
  first: Axel
  last: Steingrimsson
email: axel@gmail.com
""")
person = Person(**config)

name = Name(**config['name'])

print(person.email)
print(name.first)
