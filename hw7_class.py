
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point: Point) -> bool:
        return pow(point.x - self.x, 2) + pow(point.y - self.y, 2) <= pow(self.radius, 2)


def main():

    x, y, radius = input("Input x, y coordinates and radius of circle:").split()
    circle = Circle(int(x), int(y), int(radius))

    a, b = input("Input coordinates of point:").split()
    point = Point(int(a), int(b))
    print(circle.contains(point))


if __name__ == "__main__":
    main()
