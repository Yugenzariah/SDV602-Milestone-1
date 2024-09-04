class Status:
    """Class to manage the player's health and score."""

    def __init__(self):
        self.health: int = 100
        self.score: int = 0

    def update_score(self, points: int):
        """Update the player's score by adding points."""
        self.score += points
        print(f"Score updated: {self.score}")

    def update_health(self, amount: int):
        """Update the player's health."""
        self.health += amount
        print(f"Health updated: {self.health}")

    def show_status(self) -> str:
        """Return a string showing the player's health and score."""
        return f"Health: {self.health}\nScore: {self.score}"

if __name__ == "__main__":
    status = Status()
    status.update_score(10)
    status.update_health(-20)
    print(status.show_status())
