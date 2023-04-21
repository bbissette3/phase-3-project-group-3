import os
import colorama
import pyfiglet
import math
import time
import random
from db.models import (Base, Armor, Weapon, Specialty, Character, User)
from asceii import (chainsaw, taser_gun, poison_gas, chain_ball_whip, weapons_vault, about_us)

user_session = False
user_account = False
user_account_two = False
user_character = False
user_character_two = False

def input_centered(terminal_width):
    padding = terminal_width // 2
    print(" " * padding, end="")
    return input()

def get_user_input(choices, terminal_width):

    response = input_centered(terminal_width).title()
    if 1 <= len(response) <= 25 and choices == True or response in choices:
        return response
    else:
        print("Please Try Again")
        return get_user_input(choices, terminal_width)

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
half = int((width -25)/2)
r_align = "".rjust(half)
a_align = "".rjust(int((width-45)/2))

########################################
#Login Section
########################################
def start_menu(session):
    os.system('clear')
    global user_session
    user_session = session
    
    print_box("Welcome to BOT DECIMATION ", 34, width)
    print()
    print_centered("--- Select an Option ---", width)
    print(r_align, "1. Create New Account")
    print(r_align, "2. Login to Account")
    print(r_align, "Please Enter 1, 2, or q")
    
    response = get_user_input(["1", "2", "q"], width)

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

    user_names = [user.username.title() for user in user_session.query(User).all()]
    response = get_user_input(user_names, width)

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
    user_account = User(username = response.title())

    user_session.add(user_account)
    user_session.commit()

    print_centered(f"Congrats {user_account} Has Been Created", width)
    main_menu()

############################################
# Main Section
#############################################
def main_menu():
    os.system("clear")

    print_box("==== Main Menu ==== \n", 34, width)
    print()
    print(r_align, "1. Character Selection")
    print(r_align, "2. Battle")
    print(r_align, "3. About")
    print(r_align, "4. Log Out")
    print()

    print_centered("Please Enter 1, 2, 3 or 4", width)
    response = get_user_input(["1", "2", "3", "4"], width)

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

    with open('about.txt') as f:
        data = f.readlines()

    for line in data:
        words = line
        print(a_align, words)

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
    print(r_align,"1. Select Character")
    print(r_align,"2. Create Character")
    print(r_align,"3. Update Character")
    print(r_align,"4. Delete Character")
    print(r_align,"5. Return to Main Menu")
    print()

    print_centered("Please Enter 1, 2, 3, 4, or 5", width)
    response = get_user_input(["1", "2", "3", "4", "5"], width)

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
    for character in user_account.characters:
        print(character)
        print()
    print()
    
    print_centered("Type in Character Name", width)

    character_list = [character.name for character in current_user.characters]
    response = get_user_input(character_list, width)

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
    new_character_name= get_user_input(True, width)

#--Armor
    os.system('clear')
    print_centered("Please Type in the Name of the Armor You Want to Select", width)
    print()

    armor_selection = user_session.query(Armor.name, Armor.defense, Armor.speed).all()
    armor_strings = [f"{name}: Defense={defense}, Speed={speed}" for name, defense, speed in armor_selection]
    for armor_string in armor_strings:
        print_centered(armor_string, width)

    print()
    selected_armor_name = get_user_input((armor.name for armor in user_session.query(Armor)), width)

    selected_armor = user_session.query(Armor).filter(Armor.name == selected_armor_name).first()
    print_centered(f"You have selected {selected_armor}.", width)
    print()

#--Weapon
    os.system('clear')
    weapon_functions = [chainsaw, chain_ball_whip, poison_gas, taser_gun]
    i = 0
    print_centered("Please Type in the Name of the Weapon You Want to Select", width)
    print()
    # weapons_vault()
    print_centered("===============WEAPONS VAULT==================", width)
    weapon_selection = user_session.query(Weapon.name, Weapon.damage, Weapon.speed).all()
    weapon_strings = [f"{name}: Damage={damage}, Speed={speed}" for name, damage, speed in weapon_selection]

    for weapon_string in weapon_strings:
        weapon_functions[i]()
        print_centered(weapon_string, width)
        i += 1

    print()
    selected_weapon_name = get_user_input((weapon.name for weapon in user_session.query(Weapon).all()), width)

    selected_weapon = user_session.query(Weapon).filter(Weapon.name == selected_weapon_name).first()
    print_centered(f"You have selected {selected_weapon}.", width)
    print()

#--Specialty
    os.system('clear')
    print_centered("Please Type in the Name of the Specialty You Want to Select", width)
    print()

    specialty_selection = user_session.query(Specialty.name).all()
    specialty_strings = [f"{name}" for name, in specialty_selection]
    for specialty_string in specialty_strings:
        print_centered(specialty_string, width)

    print()
    selected_specialty_name = get_user_input([specialty.name for specialty in user_session.query(Specialty).all()], width)

    selected_specialty = user_session.query(Specialty).filter(Specialty.name == selected_specialty_name).first()
    print_centered(f"You have selected {selected_specialty}.", width)
    print()
    
    global user_character
    user_character = Character(name=new_character_name, defense=10, damage=9, speed=5, health=50, armor_id=selected_armor.id, weapon_id=selected_weapon.id, specialty_id=selected_specialty.id, user_id=user_account.id)

    user_session.add(user_character)
    user_session.commit()
    os.system('clear')
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

    print_box("==== Update Character Menu ====", 34, width)
    print()
    print_centered("--- Select an Option ---", width)
    print_centered("1. Update Character", width)
    print_centered("2. Go Back", width)
    print()

    print_centered("Please Enter 1, or 2", width)
    response = get_user_input(['1', '2'], width)

    if response == '1':

        character_list =[user.name for user in user_account.characters]
        print_centered("Character List:", width)

        for character in character_list:
            print()
            print_centered(character, width)
            print()

        print_centered("==Type in Character to Update==", width)
        response = get_user_input(character_list, width)
        
        update_character_name = user_session.query(Character).filter(Character.name== response).first()
        print_centered("Enter Characters New Name.", width)

        response = get_user_input(True, width)
        update_character_name.name = response
        user_session.commit()
        character_menu()

    elif response == '2':
        character_menu()

def delete_character():
    os.system("clear")

    print_box("==== Delete Character Menu ====", 34, width)
    print()
    print_centered("--- Select an Option ---", width)
    print_centered("1. Delete Character", width)
    print_centered("2. Go Back", width)
    print()

    print_centered("Please Enter 1, or 2", width)
    response = get_user_input(['1', '2'], width)

    if response == '1':
        os.system('clear')
        character_list = [user.name for user in user_account.characters]
        print_centered("CHARACTERS LIST:", width)

        for character in character_list:
            print()
            print_centered(character, width)
            print()

        print_centered("Type in Character Name to DELETE", width)

        response = get_user_input(character_list, width)
        delete_character_obj = user_session.query(Character).filter(Character.name == response).delete()
        
        user_session.commit()
        character_menu()

    elif response == '2':
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
    print(r_align,"1. Battle a Friend")
    print(r_align,"2. Battle Enemy")
    print(r_align,"3. The Arena")
    print(r_align,"4. Return to Main Menu")
    print()
    
    print_centered("Please Enter 1, 2, 3 or 4", width)
    response = get_user_input(['1', '2', '3', '4'], width)

    if response == '1':
        playver_v_player()
    elif response == '2':
        player_v_cpu()
    elif response == '3':
        the_arena()
    elif response == '4':
        main_menu()

def playver_v_player():
    os.system('clear')
    global user_account_two
    global user_character_two

    if user_character:
        user_account_two = log_in(False)
        user_character_two = select_character(False)
        battle_mode('0')
        battle_menu()
    else:
        print_centered("== YOU MUST SELECT A CHARACTER FIRST ==", width)
        print()
        print_centered("Moving to Character Menu ...", width)
        time.sleep(3)
        character_menu()

def player_v_cpu():
    os.system('clear')

    if user_character:

        print_box("==== BATTLE THE ENEMY ====", 34, width)
        print()
        print_centered(f"Current Character: {user_character.name}", width)
        print()
        print_centered("--- Select an Option ---", width)
        print(r_align, "1. Easy")
        print(r_align, "2. Medium")
        print(r_align, "3. Hard")
        print(r_align, "4. Return to Battle Menu")
        print()

        print_centered("Please Enter 1, 2, 3 or 4", width)
        response = get_user_input(['1', '2', '3', '4'], width)

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
        'name': user_character.name,
        "defense": (user_character.defense + user_character.armor.defense + user_character.specialty.defense),
        "damage": (user_character.damage + user_character.weapon.damage + user_character.specialty.damage),
        "speed": (user_character.speed + user_character.armor.speed + user_character.weapon.speed),
        'health': user_character.health
    }

    battle_ascii(player['name'], the_enemy['name'])

    while player["health"] > 0 and the_enemy["health"] > 0:

        if players_turn:
            turn_damage = int(random.randint((player["damage"]-5), player["damage"])*(player["speed"]/10))
            the_enemy["health"] = int(the_enemy["health"] - turn_damage*(1-(the_enemy["defense"]/100)))
            players_turn = False

            health_bar(player, the_enemy)        
            # attack_msg(player_cpu, player_one, turn_damage)
            print_centered(f"The {user_character.name}'s Turn ====", width)
            print_centered(f"{user_character.name} Deals {turn_damage} Dmg", width)
            print_centered(f"{the_enemy['name']}'s Heath is {the_enemy['health']}", width)
            print()
            time.sleep(3)
            # os.system('clear')
        else:
            turn_damage = int(random.randint((the_enemy["damage"]-5), the_enemy["damage"])   *(the_enemy["speed"]/10))
            player["health"] = int(player["health"] - turn_damage*(1-(player["defense"]/100)))
            health_bar(player, the_enemy)   
            print_centered(f"==== {the_enemy['name']}'s Turn ====", width)
            print_centered(f"{the_enemy['name']} Deals {turn_damage} Dmg", width)
            print_centered(f"{user_character.name}'s Heath is {player['health']}", width)
            print()

            players_turn = True
            time.sleep(3)
            # os.system("clear")


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
        'health': health,
        'position':[random.randint(0,9), random.randint(30,48) ],
        'movement': 10,
        'range': 1,
        'weapon': "normal",
        'attacks': "active",
        'crit_strike': 1,
        'status': ['normal', 0],
        'alternate': True, 
        'mode': None,
        'turn': False
    }

    return enemy


#THE GAME
# Implement this part last

#########################################################################################################################################
#########################################################################################################################################
#THE GAME
####################  This Function Starts ARENA ##########################
def the_arena():
    # represents key pressed by client

    if user_character:
        player_two = enemy_generator('3')

        player_one = {
            'name': user_character.name,
            "defense": (user_character.defense + user_character.armor.defense + user_character.specialty.defense),
            "damage": (user_character.damage + user_character.weapon.damage + user_character.specialty.damage),
            "speed": (user_character.speed + user_character.armor.speed + user_character.weapon.speed),
            'health': user_character.health,
            'position': [8, 19],
            'movement': 10,
            'range': 1,
            'weapon': user_character.weapon.name,
            'attacks': "active",
            'crit_strike': 1,
            'status': ['normal', 0],
            'mode': 'move',
            'turn': False
        }

        if(player_one['speed'] >= player_two['speed']):
            player_one['turn'] = True
        else:
            player_two['turn'] = True

        # This is the infinite while loop
        # Reacts based on the User's input. Until the User enters 'q'
        battle_ascii(player_one['name'], player_two['name'])
        while player_one['health'] > 0 and player_two['health'] > 0:

            os.system('clear')

            if player_one['turn']:
                players_turn(player_one, player_two)
            elif player_two['turn']:
                cpu_turn(player_two, player_one)
    else:
        os.system("clear")
        print("\n \n \n")
        print_centered("== YOU MUST SELECT A CHARACTER FIRST ==", width)
        print()
        print_centered("Moving to Character Menu ...", width)
        time.sleep(3)
        character_menu()
    if player_one['health'] <= 0:
        if player_two['health'] >= 35:
            print_centered(f"{player_two['name']} HAS CRUSHED {user_character.name} TO THE GROUND", width)
        elif player_two['health'] >= 15:
            print_centered(f"{player_two['name']} Managaed To Defeat {user_character.name}", width)
        else:
            print_centered(f"{player_two['name']} Barely Endured The Battle Against {user_character.name}", width)
    else:
        if player_one['health'] >= 35:
            print_centered(f"{user_character.name} HAS CRUSHED {player_two['name']} TO THE GROUND", width)
        elif player_one['health'] >= 15:
            print_centered(f"{user_character.name} Managaed To Defeat {player_two['name']}", width)
        else:
            print_centered(f"{user_character.name} Barely Endured The Battle Against {player_two['name']}", width)
            print()
    print_centered("PRESS ENTER TO RETURN TO MENU", width)
    input()
    
    battle_menu()





#### Calculates Dmg deducts it from Defenders Health returns Dmg #########################################
def attack_dmg(attacker, defender):
    poisoned_dmg = 0
    # Crit_strike is set to 2 if Crit is successful
    if random.randint(1,4) == 4:
        attacker['crit_strike'] = 2

    if attacker['weapon'] == 'poison gas':
        defender['status'] = ['poisoned', 2]
    elif attacker['weapon'] == 'stun gun':
        if random.randint(1,2) == 2:
            defender['status'] = ["stunned", 1]

    turn_damage = math.floor( 
        #Attack Dmg is first increased or decreased  by Attackers Speed Coefecient
        (random.randint((attacker["damage"]-5), attacker["damage"])*(attacker["speed"]/10))
        #Attack Dmg is then doubled if Attacker got a Crit
        * attacker['crit_strike'] 
        #Total DMg is then reduced by Defenders Defense coefecient
        * (1 - (defender["defense"]/100)) 
        ) 
    
    if defender['status'][0] == 'poisoned':
        poisoned_dmg = 5
        defender['status'][1] -= 1
        if defender['status'][1] == 0:
            defender['status'][1] = 'normal'
    
    defender["health"] = defender["health"] - turn_damage - poisoned_dmg
    return [turn_damage, poisoned_dmg]


########################### PRINTS OFF DAMAGE MESSAGE ##########################################
def attack_msg(attacker, defender, turn_damage): 
    if attacker['crit_strike'] == 2:
        ascii_art = pyfiglet.figlet_format("!!!!! CRIT !!!!!")
        print(ascii_art)
        attacker['crit_strike'] = 1

    print(           
    f"==== The {attacker['name']}'s Turn ==== \n" 
    + f"{attacker['name']} Deals {turn_damage[0]} Dmg \n")
    if(turn_damage[1] > 0):
        print(f"!!! {defender['name']} IS POISONED !!! \n")
        print(f"{defender['name']} suffers {turn_damage[1]} Poison Dmg.\n")
    print(f"{defender['name']}'s Heath is {defender['health']} \n \n"
    )
    # time.sleep(3)

############################# PRINTS HEALTH BAR ####################################################
def health_bar(player_one, player_two):
    # os.system('clear')
    print("".rjust(20),f"======== {player_one['name']}: {player_one['health']} ========================== {player_two['name']}: {player_two['health']} ======== \n\n\n\n")

############################# PRINTS  Starting Battle Message ####################################################
def battle_ascii(player_one, player_two):
    text = f"{player_one}\nVS\n{player_two}"

    for i in range(0,6):
        ascii_art = pyfiglet.figlet_format(text)
        print(ascii_art)

        time.sleep(0.2)
        os.system("clear")

        ascii_art = pyfiglet.figlet_format(text, font="slant")
        print(ascii_art)

        time.sleep(0.2)
        os.system("clear")

    ascii_art = pyfiglet.figlet_format("! BEGIN FIGHT !")
    print(ascii_art)

    time.sleep(1)
    os.system("clear")

####################  This Function Hands Over Control To Player ##########################
def players_turn(player_one, player_two):
    key = ''
    turn_damage = [0,0]
    player_one['movement'] = player_one['speed']
    player_one['attacks'] = 'active'

    while player_one['turn']:    
        if(key == "move"):
            player_one['mode'] = 'move'            
        elif(key =="attack"):
            player_one['mode'] = 'attack'
        elif(key == 'end'):
            player_one['turn'] = False
            player_two['turn'] = True
            return 
        
        
        if(player_one['mode'] == 'move' and player_one['movement'] > 0):
                calc_movement(key, player_one, player_two)

        elif((player_one['mode'] == 'attack') and (player_one['attacks'] == 'active')):
            if(calc_in_range(player_one, player_two)):
                turn_damage = attack_dmg(player_one, player_two)
                player_one['attacks'] = None
            else:
                pass
                # print("The Enemy Is Not In Range")

        os.system('clear')
        
        health_bar(player_one, player_two)        
        print_grid(player_one, player_two)
        attack_msg(player_one, player_two, turn_damage)
        print(f"==== Movement: {player_one['movement']} == Attacks: {player_one['attacks']}")
        print("---Select an Option ---")
        print("Enter a key:  ")
        key = input()

#########################  This Function Hands Over Control to The Computer #########################################
def cpu_turn(player_cpu, player_one):
    player_cpu['attacks'] =  'active'
    player_cpu['movement'] = player_cpu['speed']
    player_cpu['turn'] = True
    turn_damage = [0, 0]

    while player_cpu['turn']:
        if(player_cpu['movement'] > 0):
            cpu_movement(player_cpu, player_one)
        else:
            player_cpu['turn'] = False
            player_one['turn'] = True
        
        if(player_cpu['attacks'] == None):
            attack_dmg(player_cpu, player_one)
            player_cpu['turn'] = False
            player_one['turn'] = True
        os.system('clear')
        health_bar(player_one, player_cpu)        
        print_grid(player_one, player_cpu)
        attack_msg(player_cpu, player_one, turn_damage)
        time.sleep(1)


def calc_in_range(player_one, player_two):
    in_range = (player_one['position'][0] == player_two['position'][0] and 0 < abs(player_one['position'][1] - player_two["position"][1]) <= player_one['range']) \
            or (player_one['position'][1] == player_two['position'][1] and 0 < abs(player_one['position'][0] - player_two["position"][0]) <= player_one['range'])
    return in_range
    

# This function is used to calculate the player_one's new position and to reduce its movement by 1
# I didn't write any kind of if statements to prevent a player_one from moving once their
# move hits zero. So 'move' attribute is worthless now. but changing 'position' is important #######################################
def calc_movement(key, player, other_player):
    if key == "w" \
        and not(player['position'][0] -1 == other_player['position'][0] and player['position'][1] == other_player['position'][1] ):
        player['position'][0] -= 1
        player['movement'] -= 1

    if key == "s" \
        and not(player['position'][0] +1 == other_player['position'][0] and player['position'][1] == other_player['position'][1] ):
        player['position'][0] += 1
        player['movement'] -= 1

    if key == 'd' \
        and not(player['position'][1] +1 == other_player['position'][1] and player['position'][0] == other_player['position'][0] ):
        player['position'][1] += 1
        player['movement'] -= 1
    if key == 'a' \
        and not(player['position'][1] -1 == other_player['position'][1] and player['position'][0] == other_player['position'][0] ):
        player['movement'] -= 1
        player['position'][1] -= 1



#########################  Algorithm to Move CPU player Towards Player One #####################################################################
def cpu_movement(player_cpu, player_one):
    
    x, y = player_one['position'][0]-player_cpu['position'][0], player_one['position'][1]-player_cpu['position'][1]

    # print(x)
    if (y == 0 and abs(x) == 1) or (x == 0 and abs(y) == 1):
        player_cpu['attacks'] = None
        player_cpu['movement'] = 0
        return True
    elif( y == 0):
        player_cpu['alternate'] = True
    elif(x == 0):
        player_cpu['alternate'] = False

    # print(player_cpu['position'])
    if player_cpu['alternate'] or y == 0:
        player_cpu['alternate'] = False
        if x < 0:
            player_cpu['position'][0] -= 1
            player_cpu['movement'] -= 1
            return
        elif x > 0:
            player_cpu['position'][0] += 1
            player_cpu['movement'] -= 1
            return
    elif not player_cpu['alternate'] or x == 0: 
        player_cpu['alternate'] = True  
        if y < 0:
            player_cpu['position'][1] -= 1
            player_cpu['movement'] -= 1
            return
        elif y > 0:
            player_cpu['position'][1] += 1
            player_cpu['movement'] -= 1
            return



#########################  PRINTS OUT THE GRID. MAY WANT TO TURN THIS INTO A LIST #########################################
def print_grid(player_one, player_two):
#These are two loops. The first one represents the rows in the grid
#All it does is print a new line. The 2nd prints each space in in the row or column
    for row in range(11):
        for column in range(51):

# 'position' is a dict key value in User with a value pair that a list with 2 indexes.
# The [0] index represents the row position of player_one and the [1] the column
# The first if statement checks if row $ column match with player_one and enemies [0] & [1] index
# If they do they print an X to represent the player_one or enemy 
            if((row == player_one['position'][0] and column == player_one['position'][1]) or
            (row == player_two['position'][0] and column == player_two['position'][1]) ):  
                print("X", end='')

# This is a dumb feature I included. which is suppose to visually represent how much movement
# The player_one has. User[mode] reprsents if player_one is in attack mode or movement mode. Entering 'm' puts
# you in movement mode. 'a' in attack mode (I didn't think about how I was using aswd to represent
# movement and so choosing 'a' for both moving right and attack mode was dumb). Anyways if you
# 3 movement then it prints out a ^ symbol for any square thats 3 places away from you. so you
# how far you can actually movement
            elif((player_one['mode'] == 'm') and 
                ((abs(row - player_one['position'][0]) + abs(column - player_one['position'][1])) <= player_one['movement'])):
                print("^", end='')

# This just prints out a generic  '.' to represent an empty space  
            else:
                print(".", end='')

# This prints out the new line so when the first for loop repeats it will create a new row
        print("")