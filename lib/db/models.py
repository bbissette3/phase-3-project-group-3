from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

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
        return f"Id: {self.id}, " \
            + f"Name: {self.name}, " \
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
        return f"Id: {self.id}, " \
            + f"Name: {self.name}, " \
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
        return f"Id: {self.id}, " \
            + f"Name: {self.name}, " \
            + f"Defense: {self.defense}, " \
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
        return f"Id: {self.id}, " \
            + f"Name: {self.name}, " \
            + f"Defense: {self.defense}, " \
            + f"Damage: {self.damage}," \
            + f"Health: {self.health}," \
            + f"Armor Id: {self.armor_id}, " \
            + f"Weapon Id: {self.weapon_id}, " \
            + f"Speialty Id: {self.specialty_id}, " \
            + f"User Id: {self.user_id}"
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    characters = relationship("Character", backref="user")

    def __repr__(self):
        return f"Username: {self.username}"