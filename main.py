import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
from command_parser.command_parser import CommandParser
from monster_fight.monster_fight import MonsterFight
from status.status import Status
from inventory.inventory import Inventory
import random

# Game state and available places with monsters, stories, and paths
game_state: str = 'Hunted Forest'
current_monster: str = None  # Track the currently encountered monster
game_places: dict = {
    'Hunted Forest': {
        'Story': 'You are in a hunted forest.\nTo the north is a desert wasteland.\nTo the south is an abandoned castle.',
        'North': 'Desert Wasteland',
        'South': 'Abandoned Castle',
        'Image': 'hunted_forest.png',
        'Monsters': ['Zombie', 'Goblin']  # Monsters in this location
    },
    'Desert Wasteland': {
        'Story': 'You are now at the desert wasteland.\nTo the south is the hunted forest.',
        'North': '',
        'South': 'Hunted Forest',
        'Image': 'desert_wasteland.png',
        'Monsters': ['Troll']  # Monsters in this location
    },
    'Abandoned Castle': {
        'Story': 'You are now at the abandoned castle.\nTo the north is the Hunted Forest.',
        'North': 'Hunted Forest',
        'South': '',
        'Image': 'abandoned_castle.png',
        'Monsters': ['Mutant', 'Vampire']  # Monsters in this location
    },
}

def resize_image(image_path: str, max_size: tuple) -> bytes:
    """Resize the image to fit within the given max_size while maintaining the aspect ratio."""
    img = Image.open(image_path)
    img.thumbnail(max_size)
    bio = BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

def show_current_place() -> str:
    """Return the story of the current game state."""
    global game_state
    return game_places[game_state]['Story']

def make_a_window() -> sg.Window:
    """Create the game window with a layout containing the image, story, and input area."""
    
    sg.theme('Dark Blue 3')  # Set the window theme

    # Define layout components
    prompt_input = [sg.Text('Enter your command', font='Any 14'), sg.Input(key='-IN-', size=(20,1), font='Any 14', focus=True)]
    buttons = [sg.Button('Enter', bind_return_key=True), sg.Button('Exit')]
    command_col = sg.Column([prompt_input, buttons], element_justification='r')

    # Combine layout components into a window
    layout = [
        [sg.Image(resize_image(game_places['Hunted Forest']['Image'], (300, 300)), key='-IMG-')],
        [sg.Text(show_current_place(), size=(50, 4), font='Any 12', key='-OUTPUT-')],
        [command_col]
    ]

    return sg.Window('Adventure Game', layout, size=(500, 400), finalize=True)

def game_play(direction: str) -> str:
    """Update the game state based on the player's direction and return the story of the new place."""
    global game_state
    global current_monster
    current_monster = None  # Reset current monster on movement

    if direction in ['North', 'South']:
        game_place = game_places[game_state]
        proposed_state = game_place[direction]
        if proposed_state == '':
            return 'You cannot go that way.\n' + game_places[game_state]['Story']
        else:
            game_state = proposed_state
            return game_places[game_state]['Story']

def main():
    """Main game loop handling window events, player commands, and game state updates."""
    # Create the game window
    window = make_a_window()

    # Initialize systems for monster fighting, status, and inventory
    monster_fight = MonsterFight()
    monster_fight.add_monster("Zombie", 30, 5)
    monster_fight.add_monster("Mutant", 50, 8)
    monster_fight.add_monster("Goblin", 20, 3)
    monster_fight.add_monster("Troll", 60, 10)
    monster_fight.add_monster("Vampire", 40, 7)

    status = Status()
    inventory = Inventory()

    # Command parser to handle player input
    parser = CommandParser(
        game_play, 
        monster_fight, 
        game_places, 
        lambda: game_state, 
        lambda: current_monster, 
        lambda x: set_current_monster(x), 
        status,
        inventory
    )

    # Game event loop
    while True:
        event, values = window.read()

        if event == 'Enter':
            command = values['-IN-']
            result, game_over = parser.parse(command)  # Process the input command
            
            # Update the story text
            window['-OUTPUT-'].update(result)

            # If the player dies, close the game
            if game_over:
                sg.popup("You have died. Game Over.", title="Game Over")
                break

            # Update and resize the image for the new location if the game_state has changed
            resized_image = resize_image(game_places[game_state]['Image'], (300, 300))
            window['-IMG-'].update(data=resized_image)

            # Clear the input field for the next command
            window['-IN-'].update('')
            window['-IN-'].set_focus()
        
        elif event == 'Exit' or event == sg.WIN_CLOSED:
            break

    window.close()

def set_current_monster(monster: str):
    """Update the current monster encountered."""
    global current_monster
    current_monster = monster

if __name__ == "__main__":
    main()
