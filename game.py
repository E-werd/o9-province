# External
import logging, time
# Internal
from province import Province, Region
from level import LevelBase
from color import Color, ColorBase
from player import Player
from data import Data
from map import Map
from claim import Claim

class Game:
    '''Game class for o9-province'''
    def __init__(self, leveld: Data, mapd: Data, playerd: Data, map: Map) -> None:
        '''Game class for o9-province'''

        # Setup data
        logging.info("Loading data...")
        tic = time.perf_counter()

        # Setup filedata and map
        self.level_data: Data = leveld
        self.map_data: Data = mapd
        self.player_data: Data = playerd
        self.map: Map = map

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
        toc = time.perf_counter()
        logging.info(f"Loading completed! {toc - tic:0.4f}s")

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
            player = self.player_data.data[play]
            if (player["custom_color"] != None):
                r, g, b = player["custom_color"]
                color = ColorBase(name=play, rgb=(r, g, b))
                self.players.update({play: Player(name=player["name"], 
                                                  snowflake=player["snowflake"], 
                                                  color=color,
                                                  levels=self.levels)})
            else:
                self.players.update({play: Player(name=player["name"], 
                                                  snowflake=player["snowflake"], 
                                                  color=Color.list[player["color"]],
                                                  levels=self.levels)})
                
            for reg in player["owned"]["regions"]: # Iterate through regions owned
                for prov in self.regions[reg].provinces: # Iterate through provinces in the region
                    self.provinces[prov].update_owner(owner=self.players[play])
            for prov in player["owned"]["provinces"]: # Iterate through provinces owned
                self.provinces[prov].update_owner(owner=self.players[play])

    def __load_mapdata(self) -> None:
        '''Load data about maps'''
        for reg in self.map_data.data:
            self.regions.update({reg: Region(name=reg)})
            for prov in self.map_data.data[reg]:
                province = self.map_data.data[reg][prov]
                level = self.levels[province["level"]]
                x, y = province["pos"]
                self.provinces.update({prov: Province(name=prov,level=level,pos=(x,y))})
                self.regions[reg].add_province(self.provinces[prov])
                
                for adj in province["adjacent"]:
                    self.provinces[prov].add_adjacent(adj)
                
                if (province["ocean"]):
                    self.ocean_provs.append(prov)
                    self.provinces[prov].ocean = True

                if (province["sea"]):
                    for sea in province["seas"]:
                        if (sea in self.sea_provs):
                            self.sea_provs[sea].append(prov)
                        else:
                            self.sea_provs.update({sea: []})
                            self.sea_provs[sea].append(prov)
                        self.provinces[prov].sea = True
                        self.provinces[prov].seas.append(sea)

    def load_data(self) -> None:
        self.__load_levels()
        self.__load_mapdata()
        self.__load_players()

    def get_province_adjacents(self, province: Province) -> list[str]:
        raw_adjacents: list[str] = []

        if (province.ocean): # Check/Add ocean-accessible provinces
            raw_adjacents += self.ocean_provs
        
        if (province.sea): # Check/Add sea-accessible provinces
            for sea in province.seas:
                raw_adjacents += self.sea_provs[sea]

        raw_adjacents += province.adjacent # Add direct adjacents

        adjacents = list(dict.fromkeys(raw_adjacents)) # Dedupe into new list

        if province.name in adjacents:
            adjacents.remove(province.name)

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
        tic = time.perf_counter()
        self.map.add_players(players=self.players) # Send player data to map
        self.map.add_levels(levels=self.levels) # Send level data to map
        logging.info("Filling map from data...")
        for prov in self.provinces.values():
            self.map.fill(seed_point=prov.pos_xy, new_color=prov.get_color().rgb)

        toc = time.perf_counter()
        logging.info(f"Filling completed! {toc - tic:0.4f}s")

    def start(self) -> None:
        '''Main loop'''
        # Load data, update map, write map
        self.load_data()
        self.update_map()
        self.map.write()

        ### Claim example
        # for i in range(Claim.max + 1):
        #     status = Claim.check(code=i)
        #     if ( Claim.is_valid(code=i) ):
        #         logging.debug(f"Status list of code '{i}': {status}")
        #     else:
        #         logging.debug(f"Code '{i}' is invalid")

        ### Ocean/Sea example
        # print(f"Ocean provinces: {self.ocean_provs}")
        # for sea in self.sea_provs:
        #     print(f"{sea} sea provinces: {self.sea_provs[sea]}")

        ### Adjacency example
        # prov = "KS"
        # province = self.provinces[prov]
        # adjacents: list[str] = self.get_province_adjacents(province=province)
        # print(f"Provinces adjacent to '{province.name}' are: {adjacents}")

        # player = self.players["Hops"]
        # cost = self.get_cost(province=province, player=player)
        # if (cost != 0):
        #     print(f"Cost of {province.name} for {player.name} is {cost} points")
        # else: 
        #     print(f"Player '{player.name}' cannot claim '{province.name}'")