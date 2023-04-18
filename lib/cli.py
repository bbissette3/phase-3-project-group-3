from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import (Base, Armor, Weapon, Specialty, Character, User)
from helpers import (start_menu, main_menu)

if __name__ == "__main__":
    engine = create_engine("sqlite:///character_builder.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    


    start_menu(session)

