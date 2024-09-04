class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name):
        if item_name in self.items:
            self.items[item_name] += 1
        else:
            self.items[item_name] = 1
        print(f"Added {item_name} to inventory.")

    def remove_item(self, item_name):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            print(f"Removed {item_name} from inventory.")
            if self.items[item_name] == 0:
                del self.items[item_name]
        else:
            print(f"{item_name} is not in your inventory.")

    def list_inventory(self):
        print("Inventory:")
        for item, count in self.items.items():
            print(f"{item}: {count}")

if __name__ == "__main__":
    inventory = Inventory()
    inventory.add_item("medkit")
    inventory.add_item("sword")
    inventory.list_inventory()
    inventory.remove_item("medkit")
    inventory.list_inventory()
