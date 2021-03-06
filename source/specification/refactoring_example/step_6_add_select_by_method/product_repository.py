from specification.refactoring_example.step_6_add_select_by_method.product import Size, Product, Color


class ProductRepository:

    __products = []

    def add_product(self, price=0, color=Color.EMPTY, size=Size.M):
        new_product = Product(price, color, size)
        self.__products.append(new_product)

    def __iter__(self):
        return iter(self.__products)
