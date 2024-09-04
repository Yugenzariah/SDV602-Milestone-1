class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Add an item to the inventory."""
        self.items.append(item)
        print(f"Added {item} to inventory.")

    def list_inventory(self):
        """Return the list of items in the inventory."""
        return ', '.join(self.items) if self.items else 'No items in inventory'

if __name__ == "__main__":
    inventory = Inventory()
    inventory.add_item("medkit")
    inventory.add_item("sword")
    print(inventory.list_inventory())
