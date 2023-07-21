#!/usr/bin/env python3
# External
import logging, sys
from dotenv import load_dotenv
from os import getenv
# Internal
from datatypes import (ColorBase, Color, LevelBase, Level, Player, Province, Region)
from data import Data
from game import Game

class Main:
    '''Main class to run o9-province'''
    def __init__(self) -> None:
        '''Main class to run o9-province'''
        self.FILE: str = ""
        self.IMAGE: str = ""
        self.LOGLEVEL: str = ""
        
        # Load environment vars
        if not self.__load_env():
            logging.critical("Set FILE in .env, see .env.example")
            sys.exit("Exiting.")

        # Setup logging
        self.__set_logging()

        # Setup data and game
        self.data: Data = Data(file=self.FILE, source=Data.Source.json)
        self.game: Game = Game(file=self.data)

    def __load_env(self) -> bool:
        '''Loads from .env using dotenv'''
        load_dotenv()
        self.FILE = getenv("DATAFILE", default="image.json")
        self.IMAGE = getenv("IMAGEFILE", default="image.png")
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

    def start(self) -> None:
        '''Main loop'''
        x = 900
        y = 200
        # Usage example
        self.game.fill('image.png', 'colored_world_map.png', (x, y), (255, 0, 0))  # RGB for red

# Starting point
if __name__ == "__main__":
    main: Main = Main()
    main.start()