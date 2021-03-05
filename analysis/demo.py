import fitz
import pprint


class Demo:
    def __init__(self, x):
        self.x = x

    def add(self):
        return self.x + 1


class Demo2(Demo):

    def add2(self):
        return self.x + 5


# func1 = Demo(1)
func2 = Demo2(1)

# print(func1.add())
print(func2.add2())
