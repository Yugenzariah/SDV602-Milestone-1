import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
from command_parser.command_parser import CommandParser
from monster_fight.monster_fight import MonsterFight
from status.status import Status  # Import the Status class
from inventory.inventory import Inventory  # Import the Inventory class
import random

# Define the initial game state and places
game_state = 'Hunted Forest'
current_monster = None  # Track the currently encountered monster
game_places = {
    'Hunted Forest': {
        'Story': 'You are in a hunted forest.\nTo the north is a desert wasteland.\nTo the south is an abandoned castle.',
        'North': 'Desert Wasteland',
        'South': 'Abandoned Castle',
        'Image': 'hunted_forest.png',
        'Monsters': ['Zombie']  # Monsters that can appear here
    },
    'Desert Wasteland': {
        'Story': 'You are now at the desert wasteland.\nTo the south is the hunted forest.',
        'North': '',
        'South': 'Hunted Forest',
        'Image': 'desert_wasteland.png',
        'Monsters': []  # No monsters in this area
    },
    'Abandoned Castle': {
        'Story': 'You are now at the abandoned castle.\nTo the north is the Hunted Forest.',
        'North': 'Hunted Forest',
        'South': '',
        'Image': 'abandoned_castle.png',
        'Monsters': ['Mutant']  # Monsters that can appear here
    },
}

def resize_image(image_path, max_size):
    """Resize the image to fit within the max_size while keeping the aspect ratio."""
    img = Image.open(image_path)
    img.thumbnail(max_size)  # Resizes the image, keeping the aspect ratio
    bio = BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

def show_current_place():
    """Gets the story at the game_state place."""
    global game_state
    return game_places[game_state]['Story']

def make_a_window():
    """Creates the game window."""
    
    sg.theme('Dark Blue 3')  # Set the window theme
    
    # Define the layout with the input area in a separate section
    prompt_input = [sg.Text('Enter your command', font='Any 14'), sg.Input(key='-IN-', size=(20,1), font='Any 14', focus=True)]
    buttons = [sg.Button('Enter', bind_return_key=True), sg.Button('Exit')]
    command_col = sg.Column([prompt_input, buttons], element_justification='r')

    # Image and output text area
    layout = [
        [sg.Image(resize_image(game_places['Hunted Forest']['Image'], (300, 300)), key='-IMG-')],  # Resized image
        [sg.Text(show_current_place(), size=(50,4), font='Any 12', key='-OUTPUT-')],  # Story output text
        [command_col]  # The input area and buttons stay here permanently at the bottom
    ]

    return sg.Window('Adventure Game', layout, size=(500,400), finalize=True)

def game_play(direction):
    """Handles the game play by updating the game state based on direction."""
    global game_state
    global current_monster  # Reset the monster encounter when moving
    current_monster = None  # Reset current monster on movement
    if direction in ['North', 'South']:  # Check if the direction is valid
        game_place = game_places[game_state]
        proposed_state = game_place[direction]
        if proposed_state == '':
            return 'You cannot go that way.\n' + game_places[game_state]['Story']
        else:
            game_state = proposed_state
            return game_places[game_state]['Story']

def main():
    # Create the game window
    window = make_a_window()

    # Initialize the MonsterFight system
    monster_fight = MonsterFight()
    monster_fight.add_monster("Zombie", 30, 5)
    monster_fight.add_monster("Mutant", 50, 8)

    # Initialize the Status class to track score and inventory
    status = Status()

    # Initialize the Inventory class to track picked-up items
    inventory = Inventory()

    # Create an instance of CommandParser, passing game_play, monster_fight, game_places, and status
    parser = CommandParser(
        game_play, 
        monster_fight, 
        game_places, 
        lambda: game_state, 
        lambda: current_monster, 
        lambda x: set_current_monster(x), 
        status,
        inventory  # Pass inventory to the parser
    )

    # Main game loop
    while True:
        event, values = window.read()

        if event == 'Enter':
            command = values['-IN-']
            result = parser.parse(command)  # Use the parser to process the input command
            
            # Update the story text
            window['-OUTPUT-'].update(result)  # Show the command result (fight result, move result, etc.)

            # Update and resize the image for the new location if the game_state has changed
            resized_image = resize_image(game_places[game_state]['Image'], (300, 300))
            window['-IMG-'].update(data=resized_image)

            # Clear the input field and focus it again for the next command
            window['-IN-'].update('')
            window['-IN-'].set_focus()  # Ensure the input field is focused after every action
        
        elif event == 'Exit' or event == sg.WIN_CLOSED:
            break

    window.close()

# Function to update the current monster encountered
def set_current_monster(monster):
    global current_monster
    current_monster = monster

if __name__ == "__main__":
    main()
