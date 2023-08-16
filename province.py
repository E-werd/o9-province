# External
import logging
# Internal
from player import Player
from color import ColorBase
from level import LevelBase


class LevelBase:
    '''Container class for individual levels'''
    def __init__(self, name: str, cost: int, product: int, color: ColorBase):
        '''Container class for individual levels
        :name: Friendly level name
        :cost: Cost for a province at this level
        :product: How much a province at this level produces
        :color: Default color for a province at this level'''
        self.name: str = name
        self.cost: int = cost
        self.product: int = product
        self.color: ColorBase = color  
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

class Province:
    '''Class for working with provinces'''
    def __init__(self, name: str, level: LevelBase, pos: tuple = (0, 0)):
        '''Class for working with provinces
        :name: Friendly name for province
        :level: Level of province
        :pos: position on map of province, used for color filling'''
        self.name: str = name
        self.level: LevelBase = level
        self.owner: Player = None
        self.pos_xy: tuple = pos
        self.adjacent: list[str] = []
        self.ocean: bool = False
        self.sea: bool = False
        self.seas: list[str] = []

    def update_owner(self, owner: Player) -> None:
        '''Update the owner of a province
        :owner: Player object to assign as owner'''
        logging.debug(f"Updating owner for {self.name} to {owner.name}")
        self.owner = owner

    def add_adjacent(self, province: str) -> None:
        '''Add an adjacent province by name
        :province: Province name, string'''
        self.adjacent.append(province)

    def get_color(self) -> ColorBase:
        '''Returns the color object that this province should currently be.'''
        if (self.owner != None):
            logging.debug(f"Returning color for {self.name}: {str(self.owner.colors[self.level.name].rgb)}")
            return self.owner.colors[self.level.name]
        else:
            logging.debug(f"Returning color for {self.name}: {str(self.level.color.rgb)}")
            return self.level.color
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

class Region:
    '''Class for working with regions'''
    def __init__(self, name: str) -> None:
        '''Class for working with regions
        :name: Friendly name for region'''
        self.name: str = name
        self.provinces: dict[str, Province] = {}

    def add_province(self, province: Province) -> None:
        '''Add province object to region'''
        logging.debug(f"Adding province {province.name} to region {self.name}")
        self.provinces.update({province.name: province})
   
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation