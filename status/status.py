class Status:
    def __init__(self):
        self.health = 100
        self.score = 0
        self.inventory = []

    def update_score(self, points):
        self.score += points  # Add points to the score
        print(f"Score updated: {self.score}")

    def update_health(self, amount):
        self.health += amount
        print(f"Health updated: {self.health}")

    def add_item_to_inventory(self, item):
        self.inventory.append(item)  # Add picked-up item to inventory
        print(f"Added {item} to inventory.")

    def show_status(self):
        # Display health, score, and inventory
        inventory_str = ', '.join(self.inventory) if self.inventory else 'No items'
        return f"Health: {self.health}\nScore: {self.score}\nInventory: {inventory_str}"

if __name__ == "__main__":
    status = Status()
    status.update_score(10)
    status.update_health(-20)
    status.add_item_to_inventory("sword")
    print(status.show_status())
