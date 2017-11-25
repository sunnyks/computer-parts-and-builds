from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(250))
    picture = Column(String(250))



class Part(Base):
    __tablename__ = 'part'

    id = Column(Integer, primary_key = True)
    type = Column(String(40))
    name = Column(String(80), nullable = False)
    price = Column(String(10))
    manufacturer = Column(String(40))
    model_number = Column(String(100))
    #picture = Column(String(250))
    #specs/description??

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name' : self.name,
            'id' : self.id,
            'type' : self.type,
            'manufacturer' : self.manufacturer,
            'price' : self.price,
            'model_number' : self.model_number,
    }


# classes for each type of part inherit part???????????

class Motherboard(Base):
    __tablename__ = 'motherboard'

    id = Column(Integer, ForeignKey('part.id'))
    socket = Column(String(12))
    formfactor = Column(String(12))
    ramslots = Column(Integer)
    maxram = Column(String(12))

    part_info = relationship("Part", backref = "motherboard")

    @property
    def serialize(self):


class CPU(Base):
    __tablename__ = 'cpu'

    id = Column(Integer, ForeignKey('part.id'))
    speed = Column(String(12))
    cores = Column(Integer)
    tdp = Column(String(12))
    socket = Column(String(12))

    part_info = relationship("Part", backref = "cpu")

    @property
    def serialize(self):


class CPU_Cooler(Base):
    __tablename__ = 'cpu_cooler'

    id = Column(Integer, ForeignKey('part.id'))
    rpm = Column(String(50))
    noise_level = Column(String(50))

    part_info = relationship("Part", backref = "cpu_cooler")

    @property
    def serialize(self):


class Memory(Base):
    __tablename__ = 'memory'

    id = Column(Integer, ForeignKey('part.id'))
    speed = Column(String(50))
    type = Column(String(80))
    cas = Column(Integer)
    modules = Column(String(50))
    size = Column(String(80))

    part_info = relationship("Part", backref = "memory")

    @property
    def serialize(self):


class Storage(Base):
    __tablename__ = 'storage'

    id = Column(Integer, ForeignKey('part.id'))
    series = Column(String(100))
    form = Column(String(20))
    type = Column(String(20))
    capacity = Column(String(50))
    cache = Column(String(20))

    part_info = relationship("Part", backref = 'storage')

    @property
    def serialize(self):


class GPU(Base):
    __tablename__ = 'gpu'

    id = Column(Integer, ForeignKey('part.id'))
    series = Column(String(100))
    chipset = Column(String(100))
    memory = Column(String(12))
    core_clock = Column(String(12))

    part_info = relationship("Part", backref = 'gpu')

    @property
    def serialize(self):


class PowerSupply(Base):
    __tablename__ = 'power_supply'

    id = Column(Integer, ForeignKey('part.id'))
    series = Column(String(100))
    form = Column(String(12))
    efficiency = Column(String(50))
    watts = Column(String(12))
    modular = Column(String(12))

    part_info = relationship("Part", backref = 'power_supply')

    @property
    def serialize(self):

class SoundCard(Base):
    __tablename__ = 'sound_card'

    id = Column(Integer, ForeignKey('part.id'))
    chipset = Column(String(100))
    channels = Column(String(12))
    bits = Column(Integer)
    snr = Column(Integer)
    sample_rate = Column(String(20))

    part_info = relationship("Part", backref = 'sound_card')

    @property
    def serialize(self):


#class WiredNetworkCard(Part):

#class WirelessNetworkCard(Part):

#class Monitor(Part):

#class Keyboard(Part):

#class Mouse(Part):

#class AudioOut(Part):

#classes for cooling stuff? cases?


#table for wishlist
class Wishlist(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship(Part)


# table for builds

class Build(Base):
    __tablename__ = 'build'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100))
    description = Column(String(250))
    price = Column(String(15))



###########################################################################

engine = create_engine('sqlite:///computerpartsandbuilds.db')

Base.metadata.create_all(engine)
