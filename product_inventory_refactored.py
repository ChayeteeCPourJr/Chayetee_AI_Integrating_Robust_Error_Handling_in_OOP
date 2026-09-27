class InvalidProductDataError(Exception):
    """Raised when a Product is assigned invalid price or quantity data."""
    pass


class Product:
    """Represents a product with a name, price, and quantity.

    price and quantity are validated on every assignment (including in
    __init__) via @property setters, so a Product can never exist in
    an inconsistent state (e.g. a negative price or quantity).
    """

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def price(self):
        """Returns the product's price."""
        return self._price

    @price.setter
    def price(self, value):
        """Validates and sets the product's price.

        Raises:
            InvalidProductDataError: if value is not a real number,
                or if it is negative.
        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidProductDataError(
                "Price must be a number, got {}".format(type(value).__name__)
            )
        if value < 0:
            raise InvalidProductDataError(
                "Price cannot be negative, got {}".format(value)
            )
        self._price = float(value)

    @property
    def quantity(self):
        """Returns the product's quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Validates and sets the product's quantity.

        Raises:
            InvalidProductDataError: if value is not an integer,
                or if it is negative.
        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidProductDataError(
                "Quantity must be an integer, got {}".format(
                    type(value).__name__)
            )
        if value < 0:
            raise InvalidProductDataError(
                "Quantity cannot be negative, got {}".format(value)
            )
        self._quantity = value


class InventoryManager:
    """Manages the collection of products and provides inventory
    operations."""

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product):
        """Adds a product object to the inventory list."""
        self.inventory.append(product)

    def update_quantity(self, name, new_quantity):
        """Updates the quantity of a product by name.

        Because Product.quantity is a validated @property, an invalid
        new_quantity raises InvalidProductDataError here rather than
        silently corrupting the product's state.
        """
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                break

    def calculate_total_value(self):
        """Calculates the total monetary value of all inventory."""
        total = 0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        """Prints the current inventory list."""
        for product in self.inventory:
            print(f"{product.name} - ${product.price:.2f} x "
                  f"{product.quantity}")


# Demo Usage
manager = InventoryManager()
manager.add_product(Product("Laptop", 1200.00, 5))
manager.add_product(Product("Mouse", 25.00, 20))
manager.update_quantity("Mouse", 18)

print("Current Inventory:")
manager.display_inventory()
print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}")

print("\n--- Testing Invalid Input ---")
try:
    manager.inventory[0].quantity = -5
except Exception as e:
    print(f"Test result: {e}")
