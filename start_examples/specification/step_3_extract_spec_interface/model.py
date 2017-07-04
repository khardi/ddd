

class Color:
    RED = 'Red'
    GREEN = 'Green'


class Size:
    S = 'S'
    M = 'M'
    L = 'L'


class Product:

    def __init__(self, key, color, size):
        self.key = key
        self.color = color
        self.size = size


class Repository:

    __key = 0
    __products = []

    def __new_key(self):
        new_key = self.__key + 1
        self.__key = new_key
        return new_key

    def add_product(self, color, size=Size.M):
        new_product = Product(self.__new_key(), color, size)
        self.__products.append(new_product)

    def find_by_color(self, color):
        result = []
        for product in self.__products:
            if ColorSpec(color).is_satisfied_by(product):
                result.append(product)
        return result

    def find_by_size(self, size):
        result = []
        for product in self.__products:
            if SizeSpec(size).is_satisfied_by(product):
                result.append(product)
        return result


class Spec:

    def is_satisfied_by(self, color):
        raise ValueError('Base method')


class ColorSpec(Spec):

    def __init__(self, color):
        self.color = color

    def is_satisfied_by(self, product):
        return product.color == self.color


class SizeSpec(Spec):

    def __init__(self, size):
        self.size = size

    def is_satisfied_by(self, product):
        return product.size == self.size
