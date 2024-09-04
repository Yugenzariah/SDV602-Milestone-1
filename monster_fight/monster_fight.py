import random

class Monster:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def attack_player(self):
        """The monster attacks the player with random damage."""
        return random.randint(3, 10)  # Monster deals random damage between 3 and 10

class MonsterFight:
    def __init__(self):
        self.monsters = []

    def add_monster(self, name, health, attack):
        monster = Monster(name, health, attack)
        self.monsters.append(monster)

    def fight(self, monster_name, player_health):
        """Player fights the monster, and the monster attacks back."""
        for monster in self.monsters:
            if monster.name == monster_name and monster.is_alive():
                # Player deals random damage to the monster
                player_damage = random.randint(5, 15)
                monster.health -= player_damage
                fight_result = f"You dealt {player_damage} damage to {monster.name}.\n"

                # Check if the monster is defeated
                if not monster.is_alive():
                    fight_result += f"{monster.name} has been defeated!"
                    return fight_result, player_health  # Monster is dead, no need to attack player

                # Monster attacks back with random damage
                monster_damage = monster.attack_player()
                player_health -= monster_damage
                fight_result += f"{monster.name} dealt {monster_damage} damage to you.\n"

                # Check if the player is still alive
                if player_health <= 0:
                    fight_result += "You have been defeated. Game Over."
                else:
                    fight_result += f"You have {player_health} health left."
                
                return fight_result, player_health  # Return fight result and updated player health

        return f"{monster_name} is not here or already defeated.", player_health
