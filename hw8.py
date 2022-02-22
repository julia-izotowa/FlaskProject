
import math


class frange:

    def __init__(self, left: float = 0, right: float = None, step: float = 1):

        if right is None:
            self.left = 0
            self.right = left
        else:
            self.left = left
            self.right = right
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):

        if self.step > 0 and self.left >= self.right or self.step < 0 and self.left <= self.right:
            raise StopIteration()
        result = self.left
        self.left += self.step
        return result


class colorizer:

    DEFAULT = '\033[0m'
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'

    def __init__(self, color='default'):
        self.color = getattr(self, str.upper(color))

    def __enter__(self):
        print(self.color, end='')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.DEFAULT, end='')


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def square(self):
        return self.width * self.height * math.sin(self.angle)


class Triangle(Parallelogram):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width, angle)

    def square(self):
        return self.width * self.height * math.sin(self.angle) / 2


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        pass


if __name__ == "__main__":

    # Task 1
    for i in frange(1, 100, 3.5):
        print(i)
    print('\n')

    # Task 2
    with colorizer('red'):
        print('printed in red')
    print('printed in default color\n')

    # Task 3
    r = Rectangle(0, 0, 10, 20)
    r1 = Rectangle(10, 0, -10, 20)
    r2 = Rectangle(0, 20, 100, 20)
    c = Circle(10, 0, 10)
    c1 = Circle(100, 100, 5)
    p = Parallelogram(1, 2, 20, 30, 45)
    p1 = Parallelogram(1, 2, 20, 30, 45)
    t = Triangle(1, 2, 20, 30, 45)
    t1 = Triangle(1, 2, 20, 30, 45)

    scene = Scene()
    scene.add_figure(r)
    scene.add_figure(r1)
    scene.add_figure(r2)
    scene.add_figure(c)
    scene.add_figure(c1)
    scene.add_figure(p)
    scene.add_figure(p1)
    scene.add_figure(t)
    scene.add_figure(t1)

    print(f'Total square: {scene.total_square()}')
