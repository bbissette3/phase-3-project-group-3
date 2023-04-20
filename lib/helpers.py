import os
import time
import random
from db.models import (Base, Armor, Weapon, Specialty, Character, User)
from asceii import (chainsaw, taser_gun, poison_gas, chain_ball_whip, weapons_vault)

user_session = False
user_account = False
user_account_two = False
user_character = False
user_character_two = False

def get_user_input(choices):
    response = input()
    if 1<= len(response) <= 25 and choices == True or response in choices:
        return response
    else:
        print("Please Try Again")
        return get_user_input(choices)

def print_centered(text, terminal_width):
    padding = (terminal_width - len(text)) // 2
    print(" " * padding + text + " " * (terminal_width - len(text) - padding))

def print_box(text, width, terminal_width):
    padding = (terminal_width - width) // 2
    text_padding = (width - len(text) - 2) // 2  # subtract 2 for the extra spaces
    print(" " * padding + "+" + "-" * (width - 2) + "+")
    print(" " * padding + "|" + " " * (width - 2) + "|")
    print(" " * padding + "|" + " " * (text_padding + 1) + text + " " * (width - text_padding - len(text) - 3) + "|")
    print(" " * padding + "|" + " " * (width - 2) + "|")
    print(" " * padding + "+" + "-" * (width - 2) + "+")

width = os.get_terminal_size().columns

########################################
#Login Section
########################################
def start_menu(session):
    os.system('clear')
    global user_session
    user_session = session
    
    print_box("Welcome to Character Builder ", 34, width)
    print()
    print_centered("--- Select an Option ---", width)
    print_centered("1. Create New Account", width)
    print_centered("2. Login to Account", width)
    print_centered("Please Enter 1, 2, or q", width)
    
    response = get_user_input(["1", "2", "q"])

    if response == "1":
        create_account()
    elif response == "2":
        log_in(True)
    elif response == "q":
        return


def log_in(first_user):
    os.system("clear")

    users = (user_session.query(User).all())
    user_strings = [f"{user.username}" for user in users]
    for user_string in user_strings:
        print_centered(user_string, width)
    print_centered("Please Enter Your Username", width)

    user_names = [user.username for user in user_session.query(User).all()]
    response = get_user_input(user_names)

    global user_account
    user = user_session.query(User).filter(User.username == response).first()

    if first_user:
        user_account = user
        main_menu()
    else:
        return user

def create_account():
    os.system("clear")
    print_centered("Enter Your New Username", width)
    response = input()

    global user_account
    user_account = User(username = response)

    user_session.add(user_account)
    user_session.commit()

    print_centered(f"Congrats {user_account} Has Been Created", width)
    main_menu()

############################################
# Main Section
#############################################
def main_menu():
    os.system("clear")
    print_centered(str(user_account), width)

    print_box("==== Main Menu ==== \n", 34, width)
    print()
    print_centered("1. Character Selection", width)
    print_centered("2. Battle", width)
    print_centered("3. About", width)
    print_centered("4. Log Out", width)
    print()

    print_centered("Please Enter 1, 2, 3 or 4", width)
    response = get_user_input(["1", "2", "3", "4"])

    if response == "1":
        character_menu()
    elif response == "2":
        battle_menu()
    elif response == "3":
        about()
    elif response == "4":
        log_out()

def log_out():
    os.system("clear")

    global user_account 
    user_account = False
    start_menu(user_session)

def about():
    os.system("clear")
    ascii_art = '''
                ====Created By==== 
            *_   _   _   _   _   _ * 
    ^       | `_' `-' `_' `-' `_' `|       ^ 
    |       |        GROUP 3       |       | 
    |  (*)  |_   _   _   _   _   _ |  \^/  |
    | _<">_ | `_' `-' `_' `-' `_' `| _(#)_ |
    o+o \ / \\0                      0/ \ / (=)
    0'\ ^ /\/   *** Brian B ***    \/\ ^ /`0
    /_^_\ |    ** Brian R **     | /_^_\\
    || || |  **** Franco L ****  | || ||
    d|_|b_T______________________T_d|_|b
    '''
    print_centered(ascii_art, width)
    print()
    print_centered("==PRESS ENTER TO RETURN TO MAIN MENU==", width)
    input()
    main_menu()

#####################################
# Character Section
#####################################
def character_menu():
    os.system("clear")
    current_character = ''
    
    if user_character:
        current_character = user_character.name
    else:
        current_character = "None"
    

    print_box("==== Character Menu ====", 34, width)
    print()
    print_centered(f"Current Character: {current_character}", width)
    print()
    print_centered("--- Select an Option ---", width)
    print_centered("1. Select Character", width)
    print_centered("2. Create Character", width)
    print_centered("3. Update Character", width)
    print_centered("4. Delete Character", width)
    print_centered("5. Return to Main Menu", width)
    print()

    print_centered("Please Enter 1, 2, 3, 4, or 5", width)
    response = get_user_input(["1", "2", "3", "4", "5"])

    if response == "1":
        select_character(True)
    elif response == "2":
        create_character()
    elif response == "3":
        update_character()
    elif response == "4":
        delete_character()
    elif response == "5":
        main_menu()

def select_character(first_user):
    os.system("clear")
    print_box("Choose a Character", 34, width)

    current_user = None
    if first_user:
        current_user = user_account
    else:
        current_user = user_account_two

    character_list = [user.name for user in user_account.characters]
    print_centered("CHARACTERS LIST", width)
    print()
    print_centered(''.join(character_list), width)
    print()
    print_centered("Type in Character to DELETE", width)
    print()

    
    print_centered("Type in Character Name", width)

    character_list = [character.name for character in current_user.characters]
    response = get_user_input(character_list)

    character = user_session.query(Character).filter(Character.name== response).first()
    global user_character

    if first_user:
        user_character = character
        character_menu()
    else:
        return character

def create_character():
    os.system("clear")

    print_centered("Enter Your New Character Name", width)
    new_character_name= get_user_input(True)

#--Armor
    print_centered("Please Type in the Name of the Armor You Want to Select", width)
    print()

    armor_selection = user_session.query(Armor.name, Armor.defense, Armor.speed).all()
    armor_strings = [f"{name}: Defense={defense}, Speed={speed}" for name, defense, speed in armor_selection]
    for armor_string in armor_strings:
        print_centered(armor_string, width)

    print()
    selected_armor_name = get_user_input((armor.name for armor in user_session.query(Armor)))

    selected_armor = user_session.query(Armor).filter(Armor.name == selected_armor_name).first()
    print_centered(f"You have selected {selected_armor}.", width)
    print()

#--Weapon
    print_centered("Please Type in the Name of the Weapon You Want to Select", width)
    print()

    weapon_selection = user_session.query(Weapon.name, Weapon.damage, Weapon.speed).all()
    weapon_strings = [f"{name}: Damage={damage}, Speed={speed}" for name, damage, speed in weapon_selection]
    for weapon_string in weapon_strings:
        print_centered(weapon_string, width)

    print()
    selected_weapon_name = get_user_input([weapon.name for weapon in user_session.query(Weapon).all()])

    selected_weapon = user_session.query(Weapon).filter(Weapon.name == selected_weapon_name).first()
    print_centered(f"You have selected {selected_weapon}.", width)
    print()

#--Specialty
    print_centered("Please Type in the Name of the Specialty You Want to Select", width)
    print()

    specialty_selection = user_session.query(Specialty.name).all()
    specialty_strings = [f"{name}" for name, in specialty_selection]
    for specialty_string in specialty_strings:
        print_centered(specialty_string, width)

    print()
    selected_specialty_name = get_user_input([specialty.name for specialty in user_session.query(Specialty).all()])

    selected_specialty = user_session.query(Specialty).filter(Specialty.name == selected_specialty_name).first()
    print_centered(f"You have selected {selected_specialty}.", width)
    print()
    
    global user_character
    user_character = Character(name=new_character_name, defense=10, damage=9, speed=5, health=50, armor_id=selected_armor.id, weapon_id=selected_weapon.id, specialty_id=selected_specialty.id, user_id=user_account.id)

    user_session.add(user_character)
    user_session.commit()

    print_centered("New Character Created!", width)
    print()
    print_centered(f"Name: {new_character_name}", width)
    print_centered(f"Armor: {selected_armor.name} (Defense={selected_armor.defense}, Speed={selected_armor.speed})", width)
    print_centered(f"Weapon: {selected_weapon.name} (Damage={selected_weapon.damage}, Speed={selected_weapon.speed})", width)
    print_centered(f"Specialty: {selected_specialty.name}", width)
    print()
    time.sleep(3)
    character_menu()

def update_character():
    os.system("clear")

    character_list =[user.name for user in user_account.characters]
    print_centered("Character List:", width)

    for character in character_list:
        print()
        print_centered(character, width)
        print()

    print_centered("==Type in Character to Update==", width)
    response = get_user_input(character_list)
    
    update_character_name = user_session.query(Character).filter(Character.name== response).first()
    print_centered("Enter Characters New Name.", width)

    response = get_user_input(True)
    update_character_name.name = response
    user_session.commi()
    character_menu()

def delete_character():
    os.system("clear")

    character_list = [user.name for user in user_account.characters]
    print_centered("CHARACTERS LIST", width)
    print()
    print_centered(''.join(character_list), width)
    print()
    print_centered("Type in Character to DELETE", width)

    response = get_user_input(character_list)
    delete_character_obj = user_session.query(Character).filter(Character.name == response).delete()
    
    response = get_user_input(character_list)
    delete_character_obj = user_session.query(Character).filter(Character.name == response).delete()
    user_session.commit()
    character_menu()



############################################
# Battle Section
############################################
def battle_menu():
    os.system('clear')
    current_character = ''
    
    if user_character:
        current_character = user_character.name
    else:
        current_character = "None"

    print_box("==== Battle Menu ====", 34, width)
    print()
    print_centered(f"Current Character: {current_character}", width)
    print()
    print_centered("--- Select an Option ---", width)
    print_centered("1. Battle a Friend", width)
    print_centered("2. Battle Enemy", width)
    print_centered("3. Return to Main Menu", width)
    print()
    
    print_centered("Please Enter 1, 2 or 3", width)
    response = get_user_input(['1', '2', '3'])

    if response == '1':
        playver_v_player()
    elif response == '2':
        player_v_cpu()
    elif response == '3':
        main_menu()

def playver_v_player():
    os.system('clear')
    global user_account_two
    global user_character_two

    user_account_two = log_in(False)
    user_character_two = select_character(False)
    battle_mode('0')
    battle_menu()

def player_v_cpu():
    os.system('clear')

    if user_character:

        print_box("==== BATTLE THE ENEMY ====", 34, width)
        print()
        print_centered(f"Current Character: {user_character.name}", width)
        print()
        print_centered("--- Select an Option ---", width)
        print_centered("1. Easy", width)
        print_centered("2. Medium", width)
        print_centered("3. Hard", width)
        print_centered("4. Return to Battle Menu", width)
        print()

        print_centered("Please Enter 1, 2, 3 or 4", width)
        response = get_user_input(['1', '2', '3', '4'])

        if response in ['1', '2', '3']:
            battle_mode(response)
        elif response == '4':
            battle_menu()
        
    else:
        print_centered("== YOU MUST SELECT A CHARACTER FIRST ==", width)
        print()
        print_centered("Moving to Character Menu ...", width)
        time.sleep(3)
        character_menu()

#######################################################
###  BATTLE SIMULATOR
#######################################################3

def battle_mode(mode):
    os.system("clear")
    players_turn = True

    if mode == '0':
        the_enemy = {
        "name": user_character_two.name,
        "defense": (user_character_two.defense + user_character_two.armor.defense + user_character_two.specialty.defense),
        "damage": (user_character_two.damage + user_character_two.weapon.damage + user_character_two.specialty.damage),
        "speed": (user_character_two.speed + user_character_two.armor.speed + user_character_two.weapon.speed),
        'health': user_character_two.health
        }

    else:
        the_enemy = enemy_generator(mode)

    player = {
        "defense": (user_character.defense + user_character.armor.defense + user_character.specialty.defense),
        "damage": (user_character.damage + user_character.weapon.damage + user_character.specialty.damage),
        "speed": (user_character.speed + user_character.armor.speed + user_character.weapon.speed),
        'health': user_character.health
    }

    while player["health"] > 0 and the_enemy["health"] > 0:

        if players_turn:
            turn_damage = random.randint((player["damage"]-5), player["damage"])*(player["speed"]/10)
            the_enemy["health"] = the_enemy["health"] - turn_damage*(1-(the_enemy["defense"]/100))
            players_turn = False

            print_centered(f"The {user_character.name}'s Turn ====", width)
            print_centered(f"{user_character.name} Deals {turn_damage} Dmg", width)
            print_centered(f"{the_enemy['name']}'s Heath is {the_enemy['health']}", width)
            print()
            time.sleep(3)
        else:
            turn_damage = random.randint((the_enemy["damage"]-5), the_enemy["damage"])   *(the_enemy["speed"]/10)
            player["health"] = player["health"] - turn_damage*(1-(player["defense"]/100))

            print_centered(f"==== {the_enemy['name']}'s Turn ====", width)
            print_centered(f"{the_enemy['name']} Deals {turn_damage} Dmg", width)
            print_centered(f"{user_character.name}'s Heath is {player['health']}", width)
            print()

            players_turn = True
            time.sleep(3)


    if player['health'] <= 0:
        if the_enemy['health'] >= 35:
            print_centered(f"{the_enemy['name']} HAS CRUSHED {user_character.name} TO THE GROUND", width)
        elif the_enemy['health'] >= 15:
            print_centered(f"{the_enemy['name']} Managaed To Defeat {user_character.name}", width)
        else:
            print_centered(f"{the_enemy['name']} Barely Endured The Battle Against {user_character.name}", width)
    else:
        if player['health'] >= 35:
            print_centered(f"{user_character.name} HAS CRUSHED {the_enemy['name']} TO THE GROUND", width)
        elif player['health'] >= 15:
            print_centered(f"{user_character.name} Managaed To Defeat {the_enemy['name']}", width)
        else:
            print_centered(f"{user_character.name} Barely Endured The Battle Against {the_enemy['name']}", width)
            print()
    print_centered("PRESS ENTER TO RETURN TO MENU", width)
    input()
    battle_menu()

def enemy_generator(mode):
    
    defense = None
    speed = None
    damage = None
    health = 50 

    enemy_names = ["!Student", "A.I.", "Eviler Kribby", "DJ B0T", "Antonio B0T", "The Dominator"]

    if mode == '1':

        defense = random.randint(5, 15)
        speed = random.randint(5, 7)
        damage = random.randint(5, 15)
    elif mode == '2':
        defense = random.randint(20, 34)
        speed = random.randint(8, 13)
        damage = random.randint(16, 25)
    elif mode == '3':
        defense = random.randint(30, 40)
        speed = random.randint(11, 20)
        damage = random.randint(21, 30)

    enemy = {
        "name": enemy_names[random.randint(0,5)],
        "defense": defense,
        "speed": speed,
        "damage": damage,
        'health': health
    }

    return enemy


#THE GAME
# Implement this part last