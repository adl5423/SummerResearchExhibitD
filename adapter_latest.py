```python
"""
*References:
http://en.wikibooks.org/wiki/Computer_Science_Design_Patterns/Bridge_Pattern#Python

*TL;DR
Decouples an abstraction from its implementation.
"""

# ConcreteImplementor 1/2
class DrawingAPI1:
    """A drawing API implementation."""
    def draw_circle(self, x, y, radius):
        """Draw a circle with given x, y coordinates and radius."""
        print(f"API1.circle at {x}:{y} radius {radius}")

# ConcreteImplementor 2/2
class DrawingAPI2:
    """Class providing implementation of a drawing API."""
    def draw_circle(self, x, y, radius):
        """Draw a circle with given x, y coordinates and radius."""
        print(f"API2.circle at {x}:{y} radius {radius}")

    def method2(self):
        pass

# New ConcreteImplementor: Car
class Car(object):  # pylint: disable=R0903
    def vroom(self):
        print("A Car goes vroom!!!")

    def make_noise(self, octane_level):
        return f"vroom{'!' * octane_level}"

class Cat(object):
    def meow(self):
        print("A Cat goes meow!!!")

    def speak(self):
        self.meow()

class Dog(object):
    def bark(self):
        print("A Dog goes woof!!!")

    def speak(self):
        self.bark()

class Human(object):
    def speak(self):
        print("A Human speaks!!!")

    def another_public_method(self):
        pass

    def another_method(self):
        pass

class Adapter:
    pass

# Refined Abstraction
class CircleShape:
    """Class representing a circle shape."""
    def __init__(self, x, y, radius, drawing_api):
        self._x = x
        self._y = y
        self._radius = radius
        self._drawing_api = drawing_api

    def draw(self):
        """Draws the object."""
        self._drawing_api.draw_circle(self._x, self._y, self._radius)

    def scale(self, pct):
        self._radius *= pct

def main():
    shapes = (CircleShape(1, 2, 3, DrawingAPI1()), CircleShape(5, 7, 11, DrawingAPI2()))

    for shape in shapes:
        shape.scale(2.5)
        shape.draw()

    car = Car()
    car.vroom()

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
```