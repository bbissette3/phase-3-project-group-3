from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import os

width = os.get_terminal_size().columns
width = int((width - 30)/2)
r_align = "".rjust(width)

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Armor(Base):
    __tablename__ = "armors"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    speed = Column(Integer())
    defense = Column(Integer())
    characters = relationship("Character", backref=backref("armor"))

    def __repr__(self):
        return f"Type: {self.name}, " \
            + f"Speed: {self.speed}, " \
            + f"Defense: {self.defense}"
    
class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    speed = Column(Integer())
    damage = Column(Integer())
    characters = relationship("Character", backref=backref("weapon"))

    def __repr__(self):
        return f"Type: {self.name}, " \
            + f"Speed: {self.speed}, " \
            + f"Damage: {self.damage}"
    
class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    defense = Column(Integer())
    damage = Column(Integer())
    characters = relationship("Character", backref="specialty")

    def __repr__(self):
        return f"Type: {self.name}, " \
            +f"Defense: {self.defense}, " \
            + f"Damage: {self.damage}"
    
class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    defense = Column(Integer())
    damage = Column(Integer())
    speed = Column(Integer())
    health = Column(Integer())
    armor_id = Column(Integer(), ForeignKey("armors.id"))
    weapon_id = Column(Integer(), ForeignKey("weapons.id"))
    specialty_id = Column(Integer(), ForeignKey("specialties.id"))
    user_id = Column(Integer(), ForeignKey("users.id"))

    def __repr__(self):
        return r_align + f"Name: {self.name} \n" \
            + r_align + f"====== Stats ====== \n" \
            + r_align + f"Defense: Base-{self.defense} Total({self.defense + self.armor.defense + self.specialty.defense}) \n" \
            + r_align + f"Damage: Base-{self.damage} Total({self.damage + self.weapon.damage + self.specialty.damage})\n" \
            + r_align + f"Health: Base-{self.health} Total({self.health})\n" \
            + r_align + f"Speed: Base-{self.speed} Total({self.speed + self.armor.speed + self.weapon.speed}) \n" \
            + r_align + f"==== Equip \ Specialty ==== \n" \
            + r_align +f"Armor= {self.armor}, \n" \
            + r_align +f"Weapon= {self.weapon}, \n" \
            + r_align + f"Speialty= {self.specialty}, \n" \

    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    characters = relationship("Character", backref="user")

    def __repr__(self):
        return r_align +f"Username: {self.username}"