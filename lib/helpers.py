import os
import time
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

########################################
#Login Section
########################################
def start_menu(session):
    os.system("clear")
    global user_session
    user_session = session

    print( 
        f"==== Welcome to Character Builder ==== \n"  
        + f"--- Select an Option --- \n"
        + f"1. Create New Account \n"
        + f"2. Login to Account"
    )

    print("Please Enter 1, 2, or q")
    response = get_user_input(["1", "2", "q"])

    if response == "1":
        create_account()
    elif response == "2":
        log_in(True)
    elif response == "q":
        return
    
# def log_in():
#     os.system("clear")
#     print(user_session.query(User).all())
#     print("Please Enter Your Username")

#     user_names = [user.username for user in user_session.query(User).all()]
#     response = get_user_input(user_names)
#     global user_account
    
#     user_account = user_session.query(User).filter(User.username == response).first()
#     main_menu()

def log_in(first_user):
    os.system("clear")
    print(user_session.query(User).all())
    print("Please Enter Your Username")

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
    print("Enter Your New Username")
    response = input()

    global user_account
    user_account = User(username = response)

    user_session.add(user_account)
    user_session.commit()

    print("Congrats {user_account} Has Been Created")
    main_menu()


############################################
# Main Section
#############################################
def main_menu():
    os.system("clear")
    print(user_account)

    print( 
        f"==== Main Menu ==== \n"  
        + f"1. Character Selection \n"
        + f"2. Battle \n"
        + f"3. About \n"
        + f"4. Log Out"
    )

    print("Please Enter 1, 2, 3, or 4")
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
    print('''
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
    ''')
    print("==PRESS ENTER TO RETURN TO MAIN MENU==")
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
    

    print( 
        f"==== Character Menu ==== \n" 
        + f"Current Character: {current_character} \n"
        + f"--- Select an Option --- \n"
        + f"1. Select Character\n"
        + f"2. Create Character \n"
        + f"3. Update Character \n"
        + f"4. Delete Character \n"
        + f"5. Return to Main Menu"
    )

    print("Please Enter 1, 2, 3, 4, or 5")
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


# def select_character():
#     os.system("clear")
#     print("Choose a Character")
#     # print(user_session.query(Character).all())
#     for char in user_session.query(Character).all():
#         print()
#         print(char)
#     print("Type in Character Name")
#     character_list = [character.name for character in user_session.query(Character).all()]
#     response = get_user_input(character_list)
   

#     global user_character 
    
#     user_character = user_session.query(Character).filter(Character.name== response).first()
#     character_menu()


def select_character(first_user):
    os.system("clear")
    print("Choose a Character")
    # print(user_session.query(Character).all())

    # os.system("clear")
    # character_list =[user.name for user in user_account.characters]
    # print(character_list)
    # print("==Type in Character to DELETE==")
    # response = get_user_input(character_list)
    # delete_character_obj = user_session.query(Character).filter(Character.name== response).delete()    
    current_user = None
    if first_user:
        current_user = user_account
    else:
        current_user = user_account_two

    for char in current_user.characters:
        print()
        print(char)
    print("Type in Character Name")
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
    print("Enter Your New Character Name")
    new_character_name= get_user_input(True)
#--Armor
    print(" \n ==Type in Armor from list==")
   
    print(user_session.query(Armor).all())
    choose_armor = get_user_input([armor.name for armor in user_session.query(Armor).all()])

    selected_armor = user_session.query(Armor).filter(Armor.name == choose_armor).first()
    os.system("clear")
    print(f"Excellent Choice! {choose_armor}")
    print(selected_armor)
#--Weapon
    print(" \n ==Type in Weapon from list==")
    
    print(user_session.query(Weapon).all())
    choose_weapon = get_user_input([weapon.name for weapon in user_session.query(Weapon).all()])

    selected_Weapon = user_session.query(Weapon).filter(Weapon.name == choose_weapon).first()
    os.system("clear")
    print(f"Excellent Weapon Choice! {choose_weapon}")
    print(selected_Weapon)
#--Specialty
    print(" \n ==Type in Specialty from list==")
   
    print(user_session.query(Specialty).all())
    choose_specialty = get_user_input([specialty.name for specialty in user_session.query(Specialty).all()])
    
    selected_specialty = user_session.query(Specialty).filter(Specialty.name == choose_specialty).first()
    os.system("clear")
    print(f"Excellent Choice! {choose_specialty}")
    print(selected_specialty)

    global user_character
    user_character = Character(name = new_character_name, defense=10, damage=9, speed=5, health=50, armor_id=selected_armor.id, weapon_id=selected_Weapon.id, specialty_id=selected_specialty.id, user_id=user_account.id )

    user_session.add(user_character)
    user_session.commit()

    print(f"New Character {user_character} ")
    character_menu()
    

def update_character():
    os.system("clear")
    character_list =[user.name for user in user_account.characters]
    print(character_list)
    print("==Type in Character to Update==")
    response = get_user_input(character_list)
    
    
    
    update_character_name = user_session.query(Character).filter(Character.name== response).first()
    print("Enter Characters New Name.")
    response = get_user_input(True)
    update_character_name.name = response
    character_menu()

def delete_character():
    os.system("clear")
    character_list =[user.name for user in user_account.characters]
    print(character_list)
    print("==Type in Character to DELETE==")
    response = get_user_input(character_list)
    delete_character_obj = user_session.query(Character).filter(Character.name== response).delete()
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

    print( 
        f"==== Battle Menu ==== \n" 
        + f"Current Character: {current_character} \n"
        + f"--- Select an Option --- \n"
        + f"1. Battle a Friend \n"
        + f"2. Battle Enemy \n"
        + f"3. Return to Main Menu \n" 
    )
    
    print("Please Enter 1, 2 or 3")
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
        print(
        f"====  BATTLE THE ENEMY==== \n" 
        + f"Current Character: {user_character.name} \n"
        + f"--- Select an Option --- \n" 
        + f"1. Easy \n"
        + f"2. Medium \n"
        + f"3. Hard \n" 
        + f"4. Return to Battle Menu \n"
        )

        print("Please Enter 1, 2, 3, 4")
        response = get_user_input(['1', '2', '3', '4'])

        if response in ['1', '2', '3']:
            battle_mode(response)
        elif response == '4':
            battle_menu()
        
    else:
        print("== YOU MUST SELECT A CHARACTER FIRST ==")
        print("Moving to Character Menu ...")
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

    print()


    while player["health"] > 0 and the_enemy["health"] > 0:

        if players_turn:
            turn_damage = random.randint((player["damage"]-5), player["damage"])*(player["speed"]/10)
            the_enemy["health"] = the_enemy["health"] - turn_damage*(1-(the_enemy["defense"]/100))
            players_turn = False
            print(           
            f"==== The {user_character.name}'s Turn ==== \n" 
            + f"{user_character.name} Deals {turn_damage} Dmg \n"
            + f"{the_enemy['name']}'s Heath is {the_enemy['health']} \n" 
            + f" \n"
            )
            time.sleep(3)
        else:
            turn_damage = random.randint((the_enemy["damage"]-5), the_enemy["damage"])   *(the_enemy["speed"]/10)
            player["health"] = player["health"] - turn_damage*(1-(player["defense"]/100))

            print(           
            f"====  {the_enemy['name']}'s Turn ==== \n" 
            + f"{the_enemy['name']} Deals {turn_damage} Dmg \n"
            + f"{user_character.name}'s Heath is {player['health']} \n" 
            + f" \n"
            )
            players_turn = True
            time.sleep(3)



    if player['health'] <= 0:
        if the_enemy['health'] >= 35:
            print(f"{the_enemy['name']} HAS CRUSHED {user_character.name} TO THE GROUND")
        elif the_enemy['health'] >= 15:
            print(f"{the_enemy['name']} Managaed To Defeat {user_character.name}")
        else:
            print(f"{the_enemy['name']} Barely Endured The Battle Against {user_character.name}")
    else:
        if player['health'] >= 35:
            print(f"{user_character.name} HAS CRUSHED {the_enemy['name']} TO THE GROUND")
        elif player['health'] >= 15:
            print(f"{user_character.name} Managaed To Defeat {the_enemy['name']}")
        else:
            print(f"{user_character.name} Barely Endured The Battle Against {the_enemy['name']}")
    print("\n PRESS ENTER TO RETURN TO MENU ")
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