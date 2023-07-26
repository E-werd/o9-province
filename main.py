#!/usr/bin/env python3
# External
import logging, sys
from dotenv import load_dotenv
from os import getenv
# Internal
from datatypes import (ColorBase, Color, LevelBase, Player, Province, Region)
from data import Data
from map import Map

class Main:
    '''Main class to run o9-province'''
    def __init__(self) -> None:
        '''Main class to run o9-province'''
        self.DATAFILE: str = ""
        self.IMAGEFILE: str = ""
        self.PLAYERFILE: str = ""
        self.LEVELFILE: str = ""
        self.LOGLEVEL: str = ""
        
        # Load environment vars
        self.__load_env()

        # Setup logging
        self.__set_logging()

        # Setup filedata and map
        self.level_data: Data = Data(file=self.LEVELFILE, source=Data.Source.json)
        self.map_data: Data = Data(file=self.DATAFILE, source=Data.Source.json)
        self.player_data: Data = Data(file=self.PLAYERFILE, source=Data.Source.json)
        self.map: Map = Map(in_image=self.IMAGEFILE)

        # Setup data dicts
        self.regions: dict[str, Region] = {}
        self.levels: dict[str, LevelBase] = {}
        self.provinces: dict[str, Province] = {}
        self.players: dict[str, Player] = {}

        # Load in data
        self.__load_levels()
        self.__load_mapdata()
        self.__load_players()

        # Update map to current state
        self.update_map()

    def __load_env(self) -> None:
        '''Loads from .env using dotenv'''
        load_dotenv()
        self.DATAFILE = getenv("DATAFILE", default="image.json")
        self.IMAGEFILE = getenv("IMAGEFILE", default="image.png")
        self.PLAYERFILE = getenv("PLAYERFILE", default="players.json")
        self.LEVELFILE = getenv("LEVELFILE", default="levels.json")
        self.LOGLEVEL = getenv("LOGLEVEL", default="error")

    def __set_logging(self) -> None:
        '''Sets logging options'''
        logopt: dict = { "debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING , "error": logging.ERROR, "critical": logging.CRITICAL }
        format: str = "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)s] %(message)s"
        datefmt: str = "%Y-%m-%d %H:%M:%S"
        level = logopt.get(self.LOGLEVEL, logging.INFO)
        logging.basicConfig(format=format, datefmt=datefmt, level=level, force=True)

    def __load_levels(self) -> None:
        '''Load levels data, used by map data'''
        for level in self.level_data.data:
            r, g, b = self.level_data.data[level]["color"]
            level_color: ColorBase = ColorBase(name=self.level_data.data[level]["name"], rgb=(r, g, b))
            newlevel: LevelBase = LevelBase(name=self.level_data.data[level]["name"],
                                            cost=self.level_data.data[level]["cost"],
                                            product=self.level_data.data[level]["product"],
                                            color=level_color)
            self.levels.update({self.level_data.data[level]["name"]: newlevel})

    def __load_players(self) -> None:
        '''Load player data and set ownership'''
        for play in self.player_data.data:
            self.players.update({play: Player(name=play, 
                                             snowflake=self.player_data.data[play]["snowflake"], 
                                             color=Color.list[self.player_data.data[play]["color"]],
                                             levels=self.levels)})
            for reg in self.player_data.data[play]["owned"]["regions"]: # Iterate through regions owned
                for prov in self.regions[reg].provinces: # Iterate through provinces in the region
                    self.provinces[prov].update_owner(owner=self.players[play])
            for prov in self.player_data.data[play]["owned"]["provinces"]: # Iterate through provinces owned
                self.provinces[prov].update_owner(owner=self.players[play])

    def __load_mapdata(self) -> None:
        '''Load data about maps'''
        for reg in self.map_data.data:
            self.regions.update({reg: Region(name=reg)})
            for prov in self.map_data.data[reg]:
                level = self.levels[self.map_data.data[reg][prov]["level"]]
                x = self.map_data.data[reg][prov]["x"]
                y = self.map_data.data[reg][prov]["y"]
                self.provinces.update({prov: Province(name=prov,level=level,pos=(x,y))})
                self.regions[reg].add_province(self.provinces[prov])

    def update_map(self) -> None:
        for prov in self.provinces.keys():
            self.map.fill(seed_point=self.provinces[prov].pos_xy, new_color=self.provinces[prov].get_color().rgb)

    def start(self) -> None:
        '''Main loop'''
        self.map.write()

        ##Examples
        # # Get list of available colors
        # for color in Color.list:
        #     print(f"Color: {Color.list[color].name} - {Color.list[color].rgb}")

# Starting point
if __name__ == "__main__":
    main: Main = Main()
    main.start()