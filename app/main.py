#!/usr/bin/env python3
# External
import logging, os
from dotenv import load_dotenv
from pathlib import Path
# Internal
from app.core.data import Data
from app.core.map import Map
from app.core.game import Game


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
        self.FONT: str = ""
        
        # Load environment vars, logging
        self.__load_env()
        self.__set_logging()

        # Create Path objects for files
        self.datafile_path: Path = Path(self.DATAFILE).resolve()
        self.imagefile_path: Path = Path(self.IMAGEFILE).resolve()
        self.playerfile_path: Path = Path(self.PLAYERFILE).resolve()
        self.levelfile_path: Path = Path(self.LEVELFILE).resolve()
        self.font_path: Path = Path(self.FONT).resolve()

        # Setup filedata and map
        self.level_data: Data = Data(file=self.levelfile_path)
        self.map_data: Data = Data(file=self.datafile_path)
        self.player_data: Data = Data(file=self.playerfile_path)
        self.map: Map = Map(font=self.font_path, in_image=self.imagefile_path)

        # Setup game
        self.game = Game(leveld=self.level_data,
                         mapd=self.map_data,
                         playerd=self.player_data,
                         map=self.map)

    def __load_env(self) -> None:
        '''Loads from .env using dotenv'''
        load_dotenv()
        self.DATAFILE = os.getenv("DATAFILE", default="app/sample_data/image.json")
        self.IMAGEFILE = os.getenv("IMAGEFILE", default="app/sample_data/image.png")
        self.PLAYERFILE = os.getenv("PLAYERFILE", default="app/sample_data/players.json")
        self.LEVELFILE = os.getenv("LEVELFILE", default="app/sample_data/levels.json")
        self.FONT = os.getenv("FONT", default="app/sample_data/unispace.ttf")
        self.LOGLEVEL = os.getenv("LOGLEVEL", default="error")

    def __set_logging(self) -> None:
        '''Sets logging options'''
        logopt: dict = { "debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING , "error": logging.ERROR, "critical": logging.CRITICAL }
        format: str = "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)s] %(message)s"
        datefmt: str = "%Y-%m-%d %H:%M:%S"
        level = logopt.get(self.LOGLEVEL, logging.INFO)
        logging.basicConfig(format=format, datefmt=datefmt, level=level, force=True)

# Starting point
if __name__ == "__main__":
    main: Main = Main()
    main.game.start()