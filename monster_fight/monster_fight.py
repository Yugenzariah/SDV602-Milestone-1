class Monster:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

class MonsterFight:
    def __init__(self):
        self.monsters = []

    def add_monster(self, name, health, attack):
        monster = Monster(name, health, attack)
        self.monsters.append(monster)

    def fight(self, monster_name):
        for monster in self.monsters:
            if monster.name == monster_name and monster.is_alive():
                monster.health -= 10  # You attack the monster
                if monster.is_alive():
                    return f"You attack {monster.name}! It has {monster.health} health left."
                else:
                    return f"{monster.name} is defeated!"
        return f"{monster_name} is not here or already defeated."