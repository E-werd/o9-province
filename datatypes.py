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
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

class Color:
    '''Static class for colors.'''
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
    
    level1: ColorBase = ColorBase(name="level1", rgb=(0, 178, 0))
    level2: ColorBase = ColorBase(name="level2", rgb=(0, 127, 0))
    level3: ColorBase = ColorBase(name="level3", rgb=(0, 76, 0))
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

class Level:
    '''Static class for levels, will be used as a property of Province'''
    level1: LevelBase = LevelBase(name="level1", cost=5, product=1, color=Color.level1)
    level2: LevelBase = LevelBase(name="level2", cost=10, product=3, color=Color.level2)
    level3: LevelBase = LevelBase(name="level3", cost=15, product=5, color=Color.level3)
    list: dict[str, LevelBase] = {"level1": level1, "level2": level2, "level3": level3}
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

class Player:
    '''Container class for players'''
    def __init__(self, name: str, snowflake: int, color: ColorBase) -> None:
        '''Container class for players
        :name: Friendly name for player
        :snowflake: Discord user snowflake id
        :color: Base color for player provinces'''
        self.name: str = name
        self.snowflake: int = snowflake
        self.balance: int = 0
        self.color: ColorBase = color
        self.colors: dict[str, ColorBase] = self.__get_colors(base=self.color)

    def __get_colors(self, base: ColorBase) -> dict:
        '''Generate colors for each level'''
        logging.debug(f"Generating colors for {self.name} based on: {base.name} - {str(base.rgb)}")
        r, g, b = base.rgb
        colors: dict[str, ColorBase] = {}

        colors.update({"level1": ColorBase(name="level1", rgb=(r, g, b))})
        logging.debug(f"Generated color: {colors['level1'].name} - {str(colors['level1'].rgb)}")

        colors.update({"level2": ColorBase(name="level2", rgb=(round(r - (r / 6)), round(g - (g / 6)), round(b - (b / 6))))})
        logging.debug(f"Generated color: {colors['level2'].name} - {str(colors['level2'].rgb)}")

        colors.update({"level3": ColorBase(name="level3", rgb=(round(r - (r / 3)), round(g - (g / 3)), round(b - (b / 3))))})
        logging.debug(f"Generated color: {colors['level3'].name} - {str(colors['level3'].rgb)}")

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

    def update_owner(self, owner: Player) -> None:
        '''Update the owner of a province
        :owner: Player object to assign as owner'''
        logging.debug(f"Updating owner for {self.name} to {owner.name}")
        self.owner = owner

    def get_color(self) -> ColorBase:
        '''Returns the color object that this province should currently be.'''
        if (self.owner != None): 
            match self.level:
                case Level.level1:
                    logging.debug(f"Returning color for {self.name}: {str(self.owner.colors[Level.level1.name].rgb)}")
                    return self.owner.colors[Level.level1.name]
                case Level.level2:
                    logging.debug(f"Returning color for {self.name}: {str(self.owner.colors[Level.level2.name].rgb)}")
                    return self.owner.colors[Level.level2.name]
                case Level.level3:
                    logging.debug(f"Returning color for {self.name}: {str(self.owner.colors[Level.level3.name].rgb)}")
                    return self.owner.colors[Level.level3.name]
                case _: 
                    logging.debug(f"Returning color for {self.name}: {str(self.owner.color.rgb)}")
                    return self.owner.color
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