# External
import logging
from PIL import ImageColor

class ColorBase:
    '''Container class for individual colors'''
    def __init__(self, name: str, rgb: tuple) -> None:
        '''Container class for individual colors
        :name: Friendly name for color
        :rgb: 3-element tuple (r, g, b) for color'''
        self.name: str = name
        self.rgb: tuple = rgb
        logging.debug(f"Generated color: {self.name} - {str(self.rgb)}")
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

class Color:
    '''Static class for colors, provides colors by name from PIL'''
    @staticmethod
    def get_colors() -> dict[str, ColorBase]:
        all_colors: dict = ImageColor.colormap.items() # Get list of colors from PIL
        converted: dict[str, ColorBase] = {} # Declare, initialize dict

        def hex_to_rgb(hex: str) -> tuple:
            '''Convert color hex to rgb. Returns tuple'''
            h = hex.lstrip('#') # Remove pound
            return tuple(int(h[i:i+2], base=16) for i in (0, 2, 4)) # Convert each group of 2 from hexadecimal to base16

        for color in all_colors: # Loop through list of colors
            converted.update({color[0]: ColorBase(name=color[0], rgb=hex_to_rgb(color[1]))}) # Create color object, add to dict

        return converted # Return dict
    
    list: dict[str, ColorBase] = get_colors()
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

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

class Player:
    '''Container class for players'''
    def __init__(self, name: str, snowflake: int, color: ColorBase, levels: dict[str, LevelBase]) -> None:
        '''Container class for players
        :name: Friendly name for player
        :snowflake: Discord user snowflake id
        :color: Base color for player provinces'''
        self.name: str = name
        self.snowflake: int = snowflake
        self.balance: int = 0
        self.color: ColorBase = color
        self.colors: dict[str, ColorBase] = self.__get_colors(base=self.color, levels=levels)

    def __get_colors(self, base: ColorBase, levels: dict[str, LevelBase]) -> dict:
        '''Generate colors for each level'''
        logging.debug(f"Generating colors for {self.name} based on: {base.name} - {str(base.rgb)}")
        r, g, b = base.rgb
        colors: dict[str, ColorBase] = {}

        match len(levels):
            case 3:
                start = 6
                step = 4
            case _:
                start = (len(levels) * 2) - 2
                step = 2

        first: bool = True
        for _, level in levels.items():
            if (first):
                colors.update({level.name: ColorBase(name=level.name, rgb=(r, g, b))})
                first = False
            else:
                colors.update({level.name: ColorBase(name=level.name, 
                                                     rgb=(r - (r // start), 
                                                          g - (g // start), 
                                                          b - (b // start)))})
                start = start - step

        return colors
    
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