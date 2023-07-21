from PIL import ImageColor

class ColorBase:
    '''Container class for individual colors'''
    def __init__(self, name: str, rgb: list[int, int, int]) -> None:
        '''Container class for individual colors
        :name: Friendly name for color
        :rgb: 3-element list [r, g, b] for color'''
        self.name: str = name
        self.rgb: list[int, int, int] = rgb

    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"name": self.name, "rgb": self.rgb}
        return str(s)


class Color:
    '''Class for working with colors.'''
    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"level1": self.level1, "level2": self.level2, "level3": self.level3, "list": self.list}
        return str(s)
    
    @staticmethod
    def get_colors() -> dict[str, ColorBase]:
        all_colors: dict = ImageColor.colormap.items()
        converted: dict[str, ColorBase] = {}

        def hex_to_rgb(hex: str) -> list[int, int, int]:
            h = hex.lstrip('#')
            return list(int(h[i:i+2], base=16) for i in (0, 2, 4))

        for color in all_colors:
            converted.update({color[0]: ColorBase(name=color[0], rgb=hex_to_rgb(color[1]))})

        return converted
    
    level1: ColorBase = ColorBase(name="level1", rgb=[0, 178, 0])
    level2: ColorBase = ColorBase(name="level2", rgb=[0, 127, 0])
    level3: ColorBase = ColorBase(name="level3", rgb=[0, 76, 0])
    list: dict[str, ColorBase] = get_colors()

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

    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"name": self.name, "cost": self.cost, "product": self.product, "color": self.color}
        return str(s)

class Level:
    '''Class for working with levels, will be used as a property of Province'''
    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"level1": self.level1, "level2": self.level2, "level3": self.level3}
        return str(s)
    
    level1: LevelBase = LevelBase(name="level1", cost=5, product=1, color=Color.level1)
    level2: LevelBase = LevelBase(name="level2", cost=10, product=3, color=Color.level2)
    level3: LevelBase = LevelBase(name="level3", cost=15, product=5, color=Color.level3)    

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

    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"name": self.name, "snowflake": self.snowflake, "balance": self.balance, "color": self.color}
        return str(s)

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

    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"name": self.name, "level": self.level, "owner": self.owner, "pos_xy": self.pos_xy}
        return str(s)

    def update_owner(self, owner: Player) -> None:
        '''Update the owner of a province
        :owner: Player object to assign as owner'''
        self.owner = owner

    def get_color(self) -> ColorBase:
        '''Returns the color object that this province should currently be.'''
        if (self.owner != None): return self.owner.color
        else: return self.level.color

class Region:
    '''Class for working with regions'''
    def __init__(self, name: str) -> None:
        '''Class for working with regions
        :name: Friendly name for region'''
        self.name: str = name
        self.provinces: dict[str, Province] = {}

    def __repr__(self) -> str: return self.__str__()
    def __str__(self) -> str:
        s: dict = {"name": self.name, "provinces": self.provinces}
        return str(s)

    def add_province(self, province: Province) -> None:
        '''Add province object to region'''
        self.provinces.update({province.name: province})

# if __name__ == "__main__":
#     players: list[Player] = []
#     player1: Player = Player(name="player1", snowflake=8008135, color=Color.list["orange"])
#     players.append(player1)
    
#     alk: Province = Province(name="alk", level=Level.level1)
#     usa: Region = Region(name="usa")
#     usa.add_province(alk)
#     usa.provinces[alk.name].update_owner(player1)

#     print(f"{usa.provinces[alk.name].get_color().rgb}")
#     print(usa)
#     print(players)

#     color: ColorBase = random.choice(Color.list)
#     print(f"{color.name}: {color.rgb}")

#     for color in Color.list:
#         print(f"{Color.list[color].name}: {Color.list[color].rgb}")