import random

class CommandParser:
    def __init__(self, game_play, monster_fight, game_places, game_state_getter, current_monster_getter, current_monster_setter, status, inventory):
        """
        Initialize the command parser with necessary game functions, monster system, status, and inventory.
        
        Args:
            game_play: Function to handle movement in the game.
            monster_fight: Instance of MonsterFight for managing combat.
            game_places: Dictionary storing game places, stories, and monsters.
            game_state_getter: Function to get the current game state.
            current_monster_getter: Function to get the current monster.
            current_monster_setter: Function to set the current monster.
            status: Instance of Status to track player's health and score.
            inventory: Instance of Inventory to manage player's items.
        """
        self.commands = {
            "move": self.move,
            "fight": self.fight,
            "pickup": self.pickup,
            "status": self.check_status,
        }
        self.game_play = game_play
        self.monster_fight = monster_fight
        self.game_places = game_places
        self.get_game_state = game_state_getter
        self.get_current_monster = current_monster_getter
        self.set_current_monster = current_monster_setter
        self.status = status
        self.inventory = inventory

    def parse(self, command: str):
        """Parse the player's command and call the appropriate method."""
        parts = command.lower().split()
        if parts:
            action = parts[0]
            args = parts[1:]

            if action in self.commands:
                return self.commands[action](args)
            else:
                return "Unknown command. Try 'move', 'fight', 'pickup', or 'status'.", False

    def move(self, args: list):
        """Handle the player's movement command."""
        if args and args[0] in ['north', 'south']:
            result = self.game_play(args[0].capitalize())
            encounter_message = self.check_for_monster()
            return result + "\n" + encounter_message, False
        else:
            return "Invalid direction. Please use 'move north' or 'move south'.", False

    def fight(self, args: list):
        """Handle the player's fight command with the current monster."""
        current_monster = self.get_current_monster()
        if current_monster:
            if args and args[0].lower() == current_monster.lower():
                player_health = self.status.health
                fight_result, updated_health = self.monster_fight.fight(current_monster, player_health)
                self.status.update_health(updated_health - player_health)

                if updated_health <= 0:
                    fight_result += "\nYou have died. Game Over."
                    return fight_result, True  # End the game on player's death

                if "defeated" in fight_result:
                    self.status.update_score(10)
                    self.set_current_monster(None)
                    
                    # Now we make sure to always get the monsters in the location
                    monsters_in_location = self.game_places[self.get_game_state()]['Monsters']
                    
                    if current_monster in monsters_in_location:
                        monsters_in_location.remove(current_monster)

                return fight_result, False
            else:
                return f"{args[0].capitalize()} is not here or already defeated.", False
        else:
            return "There is no monster to fight.", False

    def pickup(self, args: list):
        """Handle item pickup and add it to the inventory."""
        if args:
            item = ' '.join(args)
            self.inventory.add_item(item)
            return f"You picked up a {item}.", False
        else:
            return "Specify what you want to pick up.", False

    def check_status(self, args: list):
        """Return the player's current health, score, and inventory status."""
        return f"{self.status.show_status()}\nInventory: {self.inventory.list_inventory()}", False

    def check_for_monster(self):
        """Randomly checks for a monster encounter at the current location."""
        current_state = self.get_game_state()
        monsters_in_location = self.game_places[current_state]['Monsters']

        if monsters_in_location and random.random() < 0.5:
            monster = random.choice(monsters_in_location)
            self.set_current_monster(monster)
            return f"You encounter a {monster}! Type 'fight {monster}' to engage."
        else:
            self.set_current_monster(None)
            return "No monsters here... for now."