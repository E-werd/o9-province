# External
import logging
# Internal
from color import ColorBase
from level import LevelBase


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