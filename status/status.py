class Status:
    def __init__(self):
        self.health = 100
        self.score = 0

    def update_score(self, points):
        """Update the player's score."""
        self.score += points
        print(f"Score updated: {self.score}")

    def update_health(self, amount):
        """Update the player's health."""
        self.health += amount
        print(f"Health updated: {self.health}")

    def show_status(self):
        """Return the player's health and score."""
        return f"Health: {self.health}\nScore: {self.score}"

if __name__ == "__main__":
    status = Status()
    status.update_score(10)
    status.update_health(-20)
    print(status.show_status())
