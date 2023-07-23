#!/usr/bin/env python3
# External
import logging, sys, jsons
from dotenv import load_dotenv
from os import getenv
# Internal
from datatypes import (ColorBase, Color, LevelBase, Level, Player, Province, Region)
from data import Data
from map import Map

class Main:
    '''Main class to run o9-province'''
    def __init__(self) -> None:
        '''Main class to run o9-province'''
        self.FILE: str = ""
        self.IMAGE: str = ""
        self.PLAYERS: str = ""
        self.LOGLEVEL: str = ""
        
        # Load environment vars
        if not self.__load_env():
            logging.critical("Set FILE in .env, see .env.example")
            sys.exit("Exiting.")

        # Setup logging
        self.__set_logging()

        # Setup filedata and map
        self.map_data: Data = Data(file=self.FILE, source=Data.Source.json)
        self.player_data: Data = Data(file=self.PLAYERS, source=Data.Source.json)
        self.map: Map = Map(in_image=self.IMAGE)

        # Setup data dicts
        self.regions: dict[str, Region] = {}
        self.provinces: dict[str, Province] = {}
        self.players: dict[str, Player] = {}

        # Load in data
        self.__load_mapdata()
        self.__load_players()

    def __load_env(self) -> bool:
        '''Loads from .env using dotenv'''
        load_dotenv()
        self.FILE = getenv("DATAFILE", default="image.json")
        self.IMAGE = getenv("IMAGEFILE", default="image.png")
        self.PLAYERS = getenv("PLAYERFILE", default="player.json")
        self.LOGLEVEL = getenv("LOGLEVEL", default="error")

        if (self.FILE == "none"): return False
        else: return True

    def __set_logging(self) -> None:
        '''Sets logging options'''
        logopt: dict = { "debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING , "error": logging.ERROR, "critical": logging.CRITICAL }
        format: str = "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)s] %(message)s"
        datefmt: str = "%Y-%m-%d %H:%M:%S"
        level = logopt.get(self.LOGLEVEL, logging.INFO)
        logging.basicConfig(format=format, datefmt=datefmt, level=level)

    def __load_players(self) -> None:
        '''Load player data and set ownership'''
        for play in self.player_data.data:
            self.players.update({play: Player(name=play, 
                                             snowflake=self.player_data.data[play]["snowflake"], 
                                             color=Color.list[self.player_data.data[play]["color"]])})
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
                level = Level.list[self.map_data.data[reg][prov]["level"]]
                x = self.map_data.data[reg][prov]["x"]
                y = self.map_data.data[reg][prov]["y"]
                self.provinces.update({prov: Province(name=prov,level=level,pos=(x,y))})
                self.regions[reg].add_province(self.provinces[prov])

    def start(self) -> None:
        '''Main loop'''
        for prov in self.provinces.keys():
            self.map.fill(seed_point=self.provinces[prov].pos_xy, new_color=self.provinces[prov].get_color().rgb)

        self.map.write_image()

        ##Examples
        # # Get list of available colors
        # for color in Color.list:
        #     print(f"Color: {Color.list[color].name} - {Color.list[color].rgb}")

# Starting point
if __name__ == "__main__":
    main: Main = Main()
    main.start()