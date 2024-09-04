import random

class Monster:
    """Class representing a monster with health and attack capabilities."""

    def __init__(self, name: str, health: int, attack: int):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self) -> bool:
        """Check if the monster is still alive."""
        return self.health > 0

    def attack_player(self) -> int:
        """Return random damage dealt by the monster to the player."""
        return random.randint(5, 20)

class MonsterFight:
    """System to manage monster fights and track monsters in the game."""

    def __init__(self):
        self.monsters = []

    def add_monster(self, name: str, health: int, attack: int):
        """Add a monster to the list of available monsters."""
        monster = Monster(name, health, attack)
        self.monsters.append(monster)

    def fight(self, monster_name: str, player_health: int):
        """Simulate a fight between the player and a monster."""
        for monster in self.monsters:
            if monster.name == monster_name and monster.is_alive():
                player_damage = random.randint(5, 15)
                monster.health -= player_damage
                fight_result = f"You dealt {player_damage} damage to {monster.name}.\n"

                if not monster.is_alive():
                    fight_result += f"{monster.name} has been defeated!"
                    return fight_result, player_health

                monster_damage = monster.attack_player()
                player_health -= monster_damage
                fight_result += f"{monster.name} dealt {monster_damage} damage to you.\n"

                if player_health <= 0:
                    fight_result += "You have been defeated. Game Over."
                else:
                    fight_result += f"You have {player_health} health left."

                return fight_result, player_health

        return f"{monster_name} is not here or already defeated.", player_health
