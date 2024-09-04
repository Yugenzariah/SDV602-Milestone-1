class Inventory:
    """Class to manage the player's inventory of items."""

    def __init__(self):
        self.items: list = []

    def add_item(self, item: str):
        """Add an item to the player's inventory."""
        self.items.append(item)
        print(f"Added {item} to inventory.")

    def list_inventory(self) -> str:
        """Return a string listing all items in the inventory."""
        return ', '.join(self.items) if self.items else 'No items in inventory'

if __name__ == "__main__":
    inventory = Inventory()
    inventory.add_item("medkit")
    inventory.add_item("sword")
    print(inventory.list_inventory())
