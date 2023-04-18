from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import (Base, Armor, Weapon, Specialty, Character, User)

if __name__ == "__main__":
    engine = create_engine("sqlite:///character_builder.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Armor).delete()
    session.commit()

    aluminum = Armor(name="Aluminum", speed=9, defense=3)
    diamond = Armor(name="Diamond", speed=5, defense=10)
    wood = Armor(name="Wood", speed=7, defense=7)
    gold = Armor(name="Gold", speed=6, defense=9)

    session.add(aluminum)
    session.add(diamond)
    session.add(wood)
    session.add(gold)
    session.commit()

    session.query(Weapon).delete()
    session.commit()

    chainsaw = Weapon(name="Chainsaw", speed=2, damage=10)
    chainballwhip = Weapon(name="Chain Ball Whip", speed=7, damage=10)
    poisongas = Weapon(name="Poison Gas", speed=4, damage=9)
    tasergun = Weapon(name="Taser Gun", speed=10, damage=5)

    session.add(chainsaw)
    session.add(chainballwhip)
    session.add(poisongas)
    session.add(tasergun)
    session.commit()

    session.query(Specialty).delete()
    session.commit()

    liar = Specialty(name="Liar", defense=10, damage=3)
    builder = Specialty(name="Builder", defense=8, damage=0)
    swimmer = Specialty(name="Swimmer", defense=0, damage=3)
    gentleperson = Specialty(name="Gentle Person", defense=5, damage=5)
    
    session.add(liar)
    session.add(builder)
    session.add(swimmer)
    session.add(gentleperson)
    session.commit()

    session.query(User).delete()
    session.commit()

    trollbot = User(username="Troll Bot")

    session.add(trollbot)
    session.commit()

    session.query(Character).delete()
    session.commit()

    kirby = Character(name="Kirby", defense=10, damage=9, speed=5, health=10, armor_id=gold.id, weapon_id=tasergun.id, specialty_id=liar.id, user_id=trollbot.id)

    session.add(kirby)
    session.commit()

import ipdb; ipdb.set_trace()