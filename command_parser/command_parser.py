import random

class CommandParser:
    def __init__(self, game_play, monster_fight, game_places, game_state_getter, current_monster_getter, current_monster_setter, status, inventory):
        self.commands = {
            "move": self.move,
            "fight": self.fight,
            "pickup": self.pickup,
            "status": self.check_status,
        }
        self.game_play = game_play
        self.monster_fight = monster_fight
        self.game_places = game_places  # Store game places
        self.get_game_state = game_state_getter  # Function to get current game state
        self.get_current_monster = current_monster_getter  # Function to get current monster
        self.set_current_monster = current_monster_setter  # Function to set the current monster
        self.status = status  # Reference to the Status class
        self.inventory = inventory  # Reference to the Inventory class

    def parse(self, command):
        parts = command.lower().split()  # Handle commands in lowercase
        if parts:
            action = parts[0]  # First word is the action
            args = parts[1:]    # Remaining words are arguments

            if action in self.commands:
                return self.commands[action](args)  # Call the associated method
            else:
                return "Unknown command. Try 'move', 'fight', 'pickup', or 'status'."

    def move(self, args):
        if args and args[0] in ['north', 'south']:
            result = self.game_play(args[0].capitalize())  # Move to the new location
            encounter_message = self.check_for_monster()  # Check if a monster is encountered
            return result + "\n" + encounter_message  # Return both movement and encounter result
        else:
            return "Invalid direction. Please use 'move north' or 'move south'."

    def fight(self, args):
        current_monster = self.get_current_monster()  # Check if there is an active monster
        
        if current_monster:  # If there is an active monster
            if args and args[0].lower() == current_monster.lower():  # If the player tries to fight the correct monster
                # Get player's current health
                player_health = self.status.health

                # Player fights the monster, and the monster attacks back
                fight_result, updated_health = self.monster_fight.fight(current_monster, player_health)

                # Update player's health after the fight
                self.status.update_health(updated_health - player_health)

                # If the monster is defeated, update the score and clear the current_monster
                if "defeated" in fight_result:
                    self.status.update_score(10)  # Award points for defeating the monster
                    self.set_current_monster(None)

                return fight_result  # Return the fight result and updated health
            else:
                return f"{args[0].capitalize()} is not here or already defeated."
        else:
            return "There is no monster to fight."

    def pickup(self, args):
        if args:
            item = ' '.join(args)
            self.inventory.add_item(item)  # Add the item to the player's inventory
            return f"You picked up a {item}."
        else:
            return "Specify what you want to pick up."

    def check_status(self, args):
        # Combine the status (health, score) with the inventory
        return f"{self.status.show_status()}\nInventory: {self.inventory.list_inventory()}"

    def check_for_monster(self):
        """Randomly checks for a monster encounter at the current location."""
        current_state = self.get_game_state()  # Get current game state
        monsters_in_location = self.game_places[current_state]['Monsters']

        if monsters_in_location and random.random() < 0.5:  # 50% chance to encounter
            monster = random.choice(monsters_in_location)  # Pick a random monster from the location
            self.set_current_monster(monster)  # Set this monster as the current monster
            return f"You encounter a {monster}! Type 'fight {monster}' to engage."
        else:
            self.set_current_monster(None)  # Ensure no monster is set if none is found
            return "No monsters here... for now."
