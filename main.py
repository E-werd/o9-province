#!/usr/bin/env python3
# External
import logging, os, time
from dotenv import load_dotenv
from pathlib import Path
# Internal
from datatypes import (ColorBase, Color, LevelBase, Player, Province, Region)
from data import Data
from map import Map

class Status:
    class Claim:
        ok = 1
        water = 2
        self_owned = 4
        other_owned = 8
        not_adjacent = 16

class Main:
    '''Main class to run o9-province'''
    def __init__(self) -> None:
        '''Main class to run o9-province'''
        print("Setting up environment...")
        self.DATAFILE: str = ""
        self.IMAGEFILE: str = ""
        self.PLAYERFILE: str = ""
        self.LEVELFILE: str = ""
        self.LOGLEVEL: str = ""
        
        # Load environment vars
        self.__load_env()

        # Setup logging
        self.__set_logging()
        logging.info("Loading data...")
        tic = time.perf_counter()

        # Create Path objects for files
        self.datafile_path: Path = Path(self.DATAFILE).resolve()
        self.imagefile_path: Path = Path(self.IMAGEFILE).resolve()
        self.playerfile_path: Path = Path(self.PLAYERFILE).resolve()
        self.levelfile_path: Path = Path(self.LEVELFILE).resolve()

        # Setup filedata and map
        self.level_data: Data = Data(file=self.levelfile_path)
        self.map_data: Data = Data(file=self.datafile_path)
        self.player_data: Data = Data(file=self.playerfile_path)
        self.map: Map = Map(in_image=self.imagefile_path)

        # Setup data dicts
        self.regions: dict[str, Region] = {}
        self.levels: dict[str, LevelBase] = {}
        self.provinces: dict[str, Province] = {}
        self.players: dict[str, Player] = {}
        self.ocean_provs: list[str] = []
        self.sea_provs: dict[str, list[str]] = {}

        # Load in data
        self.__load_levels()
        self.__load_mapdata()
        self.__load_players()

        # Update map to current state
        self.update_map()
        toc = time.perf_counter()
        logging.info(f"Loading completed! {toc - tic:0.4f}s")

    def __load_env(self) -> None:
        '''Loads from .env using dotenv'''
        load_dotenv()
        self.DATAFILE = os.getenv("DATAFILE", default="image.json")
        self.IMAGEFILE = os.getenv("IMAGEFILE", default="image.png")
        self.PLAYERFILE = os.getenv("PLAYERFILE", default="players.json")
        self.LEVELFILE = os.getenv("LEVELFILE", default="levels.json")
        self.LOGLEVEL = os.getenv("LOGLEVEL", default="error")

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
                x, y = self.map_data.data[reg][prov]["pos"]
                self.provinces.update({prov: Province(name=prov,level=level,pos=(x,y))})
                self.regions[reg].add_province(self.provinces[prov])
                
                for adj in self.map_data.data[reg][prov]["adjacent"]:
                    self.provinces[prov].add_adjacent(adj)
                
                if (self.map_data.data[reg][prov]["ocean"]):
                    self.ocean_provs.append(prov)
                    self.provinces[prov].ocean = True

                if (self.map_data.data[reg][prov]["sea"]):
                    for sea in self.map_data.data[reg][prov]["seas"]:
                        if (sea in self.sea_provs):
                            self.sea_provs[sea].append(prov)
                        else:
                            self.sea_provs.update({sea: []})
                            self.sea_provs[sea].append(prov)
                        self.provinces[prov].sea = True
                        self.provinces[prov].seas.append(sea)

    def get_province_adjacents(self, province: Province) -> list[str]:
        raw_adjacents: list[str] = []

        if (province.ocean): # Check/Add ocean-accessible provinces
            raw_adjacents += self.ocean_provs
        
        if (province.sea): # Check/Add sea-accessible provinces
            for sea in province.seas:
                raw_adjacents += self.sea_provs[sea]

        raw_adjacents += province.adjacent # Add direct adjacents

        adjacents = list(dict.fromkeys(raw_adjacents)) # Dedupe into new list
        return adjacents
    
    def get_player_adjacents(self, player: Player) -> list[str]:
        raw_adjacents: list[str] = []
        owned_provinces: list[str] = []

        for prov in self.provinces: # Get owned provinces
            if (self.provinces[prov].owner == player):
                owned_provinces.append(prov)
        
        for prov in owned_provinces: # Get adjacents of owned provinces
            raw_adjacents += self.get_province_adjacents(province=self.provinces[prov])

        adjacents = list(dict.fromkeys(raw_adjacents)) # Dedupe into new list

        for prov in adjacents:
            try:
                provin = self.provinces[prov]
            except (KeyError):
                continue # Not in the data list yet, move on for now.

            if (provin.owner != None): # Remove if owned by anybody
                adjacents.remove(prov)
        
        return adjacents
    
    def get_cost(self, province: Province, player: Player) -> int:
        adjacents: list[str] = self.get_player_adjacents(player=player)
        if (province.owner == player):
            return 0
        elif (province.owner != None):
            return 0

        if province.name in adjacents:
            if province.name not in province.adjacent:
                return province.level.cost * 2
            else:
                return province.level.cost
        else:
            return 0

    def update_map(self) -> None:
        '''Fill in map from latest data'''
        logging.info("Filling map from data...")
        for prov in self.provinces.keys():
            self.map.fill(seed_point=self.provinces[prov].pos_xy, new_color=self.provinces[prov].get_color().rgb)

    def start(self) -> None:
        '''Main loop'''
        self.map.write()

        # print(f"Ocean provinces: {self.ocean_provs}")
        # for sea in self.sea_provs:
        #     print(f"{sea} sea provinces: {self.sea_provs[sea]}")

        # prov = "QUE"
        # province = self.provinces[prov]
        # player = self.players["player2"]
        # cost = self.get_cost(province=province, player=player)
        # if (cost != 0):
        #     print(f"Cost of {province.name} for {player.name} is {cost} points")
        # else: 
        #     print(f"Player '{player.name}' cannot claim '{province.name}'")

        ##Examples
        # # Get list of available colors
        # for color in Color.list:
        #     print(f"Color: {Color.list[color].name} - {Color.list[color].rgb}")

# Starting point
if __name__ == "__main__":
    main: Main = Main()
    main.start()