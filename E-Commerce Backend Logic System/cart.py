from typing import Dict, Any

class ShoppingCart:
    def __init__(self):
        # Format: { product_id: {"id": int, "name": str, "price": float, "quantity": int, "stock": int} }
        self.items: Dict[int, Dict[str, Any]] = {}

    def add_item(self, product_id: int, name: str, price: float, quantity: int, stock: int) -> bool:
        """Adds a product to the cart or updates quantity if already added."""
        if quantity <= 0:
            print("\nError: Quantity must be greater than zero.")
            return False

        current_cart_qty = self.items[product_id]["quantity"] if product_id in self.items else 0
        total_requested = current_cart_qty + quantity

        if total_requested > stock:
            print(f"\nError: Insufficient stock. Available: {stock}, Already in cart: {current_cart_qty}.")
            return False

        if product_id in self.items:
            self.items[product_id]["quantity"] += quantity
        else:
            self.items[product_id] = {
                "id": product_id,
                "name": name,
                "price": price,
                "quantity": quantity,
                "stock": stock
            }
        print(f"\nSuccess: Added {quantity} unit(s) of '{name}' to cart.")
        return True

    def remove_item(self, product_id: int) -> bool:
        """Removes an item completely from the cart."""
        if product_id in self.items:
            removed = self.items.pop(product_id)
            print(f"\nSuccess: Removed '{removed['name']}' from cart.")
            return True
        else:
            print(f"\nError: Product ID {product_id} is not in your cart.")
            return False

    def update_quantity(self, product_id: int, new_quantity: int) -> bool:
        """Updates the quantity of an item in the cart."""
        if product_id not in self.items:
            print(f"\nError: Product ID {product_id} is not in your cart.")
            return False

        if new_quantity <= 0:
            return self.remove_item(product_id)

        available_stock = self.items[product_id]["stock"]
        if new_quantity > available_stock:
            print(f"\nError: Cannot set quantity to {new_quantity}. Available stock is {available_stock}.")
            return False

        self.items[product_id]["quantity"] = new_quantity
        print(f"\nSuccess: Updated quantity for '{self.items[product_id]['name']}' to {new_quantity}.")
        return True

    def calculate_total(self) -> float:
        """Calculates the total bill amount for items in the cart."""
        return sum(item["price"] * item["quantity"] for item in self.items.values())

    def clear(self):
        """Clears all items from the cart."""
        self.items.clear()

    def is_empty(self) -> bool:
        """Checks if the cart contains any items."""
        return len(self.items) == 0