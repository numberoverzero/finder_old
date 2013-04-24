def inject(obj, funcs=None):
    '''
    funcs is a dictionary of functions to inject,
    and is passed directly to type for constructing a new class.
    type(inject(obj)) == type(obj)

    does not work for objects without a __dict__ value, such as list and dict.

    class Person(object):
        def __init__(self, name):
            self.name = name
        def speak(self):
            print "My name is {}.".format(self.name)

    def speak(self, other):
        print "Hello {}.  My name is {}.".format(other, self.name)

    jim = Person("Jim")
    friendly_jim = inject(jim, 'speak':speak)

    jim.speak()  # prints "My name is Jim."
    friendly_jim.speak()  # TypeError because speak now takes two arguments
    friendly_jim.speak("Bill")  # prints "Hello Bill.  My name is Jim."
    '''
    funcs = funcs or {}
    cls = obj.__class__
    name = cls.__name__

    class Injected(cls):
        def __init__(self, obj):
            bases = Injected, cls
            self.__class__ = type(name, bases, funcs)

            try:
                self.__dict__ = obj.__dict__
            except AttributeError:
                raise AttributeError("Can't inject an object without a __dict__.")
    return Injected(obj)
