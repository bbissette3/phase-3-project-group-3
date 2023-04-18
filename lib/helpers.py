import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import (Base, Armor, Weapon, Specialty, Character, User)


user_session = False
user_account = False

def get_user_input(choices):
    response = input()
    if response in choices:
        return response
    else:
        print("Please Try Again")
        return False


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
    elif response == False:
        start_menu(user_session)

def log_in():
    os.system("clear")
    print(user_session.query(User).all())
    print("Please Enter Your Username")

    user_names = [user.username for user in user_session.query(User).all()]
    response = get_user_input(user_names)
    global user_account

    if response == False:
        log_in()
    else: 
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
    print("Success")
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
    elif response == False:
        main_menu()

def log_out():
    os.system("clear")
    print("log Out?")

def about():
    os.system("clear")
    print("About Us")


# Character Section
def character_menu():
    os.system("clear")
    print("select an Option")

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
    elif response == False:
        character_menu()

def select_character():
    os.system("clear")
    print("Choose a Character")
    print(user_session.query(Character).all())

    character_list = [character.name for character in user_session.query(Character).all()]
    response = get_user_input(character_list)
    print(response)

def create_character():
    print("make new character")

def update_character():
    print("update character")

def delete_character():
    print("delete character")


# Battle Section
def battle_menu():
    print("Battle!")

def playver_v_player():
    pass

def player_v_cpu():
    pass




#THE GAME
# Implement this part last