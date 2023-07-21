# External
from PIL import ImageColor

class ColorBase:
    '''Container class for individual colors'''
    def __init__(self, name: str, rgb: list[int, int, int]) -> None:
        '''Container class for individual colors
        :name: Friendly name for color
        :rgb: 3-element list [r, g, b] for color'''
        self.name: str = name
        self.rgb: list[int, int, int] = rgb
        # Update this when class properties change!
        self.__s: dict = {"name": self.name, "rgb": self.rgb}

    # Return a dict/json compatible string representation of this object.
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation


class Color:
    '''Static class for colors.'''
    @staticmethod
    def get_colors() -> dict[str, ColorBase]:
        all_colors: dict = ImageColor.colormap.items() # Get list of colors from PIL
        converted: dict[str, ColorBase] = {} # Declare, initialize dict

        def hex_to_rgb(hex: str) -> list[int, int, int]:
            '''Convert color hex to rgb'''
            h = hex.lstrip('#') # Remove pound
            return list(int(h[i:i+2], base=16) for i in (0, 2, 4)) # Convert each group of 2 from hexadecimal to base16

        for color in all_colors: # Loop through list of colors
            converted.update({color[0]: ColorBase(name=color[0], rgb=hex_to_rgb(color[1]))}) # Create color object, add to dict

        return converted # Return dict
    
    level1: ColorBase = ColorBase(name="level1", rgb=[0, 178, 0])
    level2: ColorBase = ColorBase(name="level2", rgb=[0, 127, 0])
    level3: ColorBase = ColorBase(name="level3", rgb=[0, 76, 0])
    list: dict[str, ColorBase] = get_colors()

    # Return a dict/json compatible string representation of this object.
    # Update this when class properties change!
    __s: dict = {"level1": level1, "level2": level2, "level3": level3, "list": list}
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation

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
        # Update this when class properties change!
        self.__s: dict = {"name": self.name, "cost": self.cost, "product": self.product, "color": self.color}
    
    # Return a dict/json compatible string representation of this object.
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation

class Level:
    '''Static class for levels, will be used as a property of Province'''
    level1: LevelBase = LevelBase(name="level1", cost=5, product=1, color=Color.level1)
    level2: LevelBase = LevelBase(name="level2", cost=10, product=3, color=Color.level2)
    level3: LevelBase = LevelBase(name="level3", cost=15, product=5, color=Color.level3)

    # Return a dict/json compatible string representation of this object.
    # Update this when class properties change!
    __s: dict = {"level1": level1, "level2": level2, "level3": level3}
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation

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
        # Update this when class properties change!
        self.__s: dict = {"name": self.name, "snowflake": self.snowflake, "balance": self.balance, "color": self.color}

    # Return a dict/json compatible string representation of this object.
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation

class Province:
    '''Class for working with provinces'''
    def __init__(self, name: str, level: LevelBase, pos: list[int, int]=[0, 0]):
        '''Class for working with provinces
        :name: Friendly name for province
        :level: Level of province
        :pos: position on map of province, used for color filling'''
        self.name: str = name
        self.level: LevelBase = level
        self.owner: Player = None
        self.pos_xy: list[int, int] = pos
        # Update this when class properties change!
        self.__s: dict = {"name": self.name, "level": self.level, "owner": self.owner, "pos_xy": self.pos_xy}

    def update_owner(self, owner: Player) -> None:
        '''Update the owner of a province
        :owner: Player object to assign as owner'''
        self.owner = owner

    def get_color(self) -> ColorBase:
        '''Returns the color object that this province should currently be.'''
        if (self.owner != None): return self.owner.color
        else: return self.level.color

    # Return a dict/json compatible string representation of this object.
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation

class Region:
    '''Class for working with regions'''
    def __init__(self, name: str) -> None:
        '''Class for working with regions
        :name: Friendly name for region'''
        self.name: str = name
        self.provinces: dict[str, Province] = {}
        # Update this when class properties change!
        self.__s: dict = {"name": self.name, "provinces": self.provinces}

    def add_province(self, province: Province) -> None:
        '''Add province object to region'''
        self.provinces.update({province.name: province})

    # Return a dict/json compatible string representation of this object.
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __dict__(self) -> dict: return self.__s # Dictionary representation
    def __str__(self) -> str: return str(self.__s) # String representation

# Examples
## Create a player list, a player object, and add the object to the list
#players: list[Player] = []
#player1: Player = Player(name="player1", snowflake=8008135, color=Color.list["orange"])
#players.append(player1)

## Create a province object, a region object, add province to region, and add owner to province
#alk: Province = Province(name="alk", level=Level.level1)
#usa: Region = Region(name="usa")
#usa.add_province(alk)
#usa.provinces[alk.name].update_owner(player1)

## Print representations of region, player list
#print(f"{usa.provinces[alk.name].get_color().rgb}")
#print(usa)
#print(players)

## Get a random color, print name and rgb representation
#color: ColorBase = random.choice(Color.list)
#print(f"{color.name}: {color.rgb}")

## For all colors, print name and rgb representation
#for color in Color.list:
#    print(f"{Color.list[color].name}: {Color.list[color].rgb}")