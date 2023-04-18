import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import (Base, Armor, Weapon, Specialty, Character, User)


user_session = False
user_account = False
user_character = False

def get_user_input(choices):
    response = input()
    if 1<= len(response) <= 25 and choices == True or response in choices:
        return response
    else:
        print("Please Try Again")
        return get_user_input(choices)


#Login Section
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
        log_in()
    elif response == "q":
        return
    
def log_in():
    os.system("clear")
    print(user_session.query(User).all())
    print("Please Enter Your Username")

    user_names = [user.username for user in user_session.query(User).all()]
    response = get_user_input(user_names)
    global user_account
    
    user_account = user_session.query(User).filter(User.username == response).first()
    main_menu()

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



# Main Section
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
o+o \ / \0                      0/ \ / (=)
 0'\ ^ /\/     ** Brian B **    \/\ ^ /`0
   /_^_\ |     ** Brian R **    | /_^_|
   || || |     ** Franco L **   | || ||
   d|_|b_T______________________T_d|_|b
    ''')
    print("==PRESS ENTER TO RETURN TO MAIN MENU==")
    input()
    main_menu()


# Character Section
def character_menu():
    os.system("clear")
    

    print( 
        f"==== Character Menu ==== \n" 
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
        select_character()
    elif response == "2":
        create_character()
    elif response == "3":
        update_character()
    elif response == "4":
        delete_character()
    elif response == "5":
        main_menu()


def select_character():
    os.system("clear")
    print("Choose a Character")
    print(user_session.query(Character).all())
    print("Type in Character Name")
    character_list = [character.name for character in user_session.query(Character).all()]
    response = get_user_input(character_list)
   

    global user_character 
    
    user_character = user_session.query(Character).filter(Character.name== response).first()
    character_menu()

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
    user_character = Character(name = new_character_name, defense=10, damage=9, speed=5, health=10, armor_id=selected_armor.id, weapon_id=selected_Weapon.id, specialty_id=selected_specialty.id, user_id=user_account.id )

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



# Battle Section
def battle_menu():
    print("Battle!")

def playver_v_player():
    pass

def player_v_cpu():
    pass




#THE GAME
# Implement this part last