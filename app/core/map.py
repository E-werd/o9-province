#!/usr/bin/env python3
# External
import logging, time
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from scipy.ndimage import label
from pathlib import Path
# Internal
from app.core.player import Player
from app.core.province import LevelBase


class Map:
    '''Class for loading/creating/filling maps'''
    def __init__(self, font: Path, in_image: Path, out_image: Path = None) -> None:
        '''Class for loading/creating/filling maps
        :font: path to font for legend
        :in_image: path to base image
        :out_image: path to output image'''
        self.font_path: Path = font.resolve()
        self.in_image_path: Path = in_image
        self.out_image_path: Path = out_image
        self.players: dict[str, Player] = {}
        self.levels: dict[str, LevelBase] = {}
        
        # Check if output path set, if not set at input path
        if (self.out_image_path == None):
            out_stem: str = "out_" + self.in_image_path.stem
            self.out_image_path = self.in_image_path.with_stem(stem=out_stem).resolve()

        # Load the input image
        logging.info(f"Loading map image from file: {self.in_image_path}")
        self.image: np.ndarray = self.__get_image_array(img_path=self.in_image_path)

    def __get_image_array(self, img_path: str) -> np.ndarray:
        '''Convert image to numpy array
        :img_path: Path of image to load'''
        # Open image and convert to RGB
        img = Image.open(fp=img_path, mode="r").convert("RGB") # Returns PIL.Image.Image object

        # Convert image data to numpy array
        img_array = np.array(object=img) # returns np.ndarray object, basically just an array
        return img_array
    
    def add_players(self, players: dict[str, Player]):
        '''Set players for map legend
        :players: dict with list of players'''
        self.players = players
    
    def add_levels(self, levels: dict[str, LevelBase]):
        '''Set levels for map legend
        :levels: dict with list of levels'''
        self.levels = levels

    def write(self, dest: Path = None) -> None:
        '''Write map image to destination
        :dest: Destination path for the image'''
        # Convert array to image
        self.draw_legend()
        new_image = Image.fromarray(obj=np.uint8(self.image))

        # Save the output image
        if (dest == None): 
            logging.info(f"Writing map to {self.out_image_path.__str__()}")
            new_image.save(self.out_image_path.__str__())
        else: 
            logging.info(f"Writing map to {dest.__str__()}")
            new_image.save(dest.__str__())

    def fill(self, seed_point: tuple, new_color: tuple) -> None:
        '''Fill a province
        :seed_point: (x,y) position inside a province
        :new_color: (r,g,b) value to fill'''
        logging.debug(f"Filling province at {str(seed_point)} with color {str(new_color)}")

        tic = time.perf_counter()
        # Get color at the seed_point
        seed_color = self.image[seed_point[1], seed_point[0]] # Gets pixel in rgb at image coords [y, x]
        toc = time.perf_counter()
        logging.debug(f"Color time: {toc - tic:0.4f}s")

        tic = time.perf_counter()
        # Generate a binary image (mask) where pixels with the seed color are white
        mask = np.all(self.image == seed_color, axis=-1)
        toc = time.perf_counter()
        logging.debug(f"Binary image time: {toc - tic:0.4f}s")
        logging.debug(f"Binary image size: {np.array(object=mask).shape}")

        tic = time.perf_counter()
        # Label all connected regions in the mask
        labeled_array, num_features = label(input=mask)
        toc = time.perf_counter()
        logging.debug(f"Label1 time: {toc - tic:0.4f}s")
        logging.debug(f"Label1 size: {np.array(object=labeled_array).shape}")

        tic = time.perf_counter()
        # Get label of the region where seed_point is located
        seed_label = labeled_array[seed_point[1], seed_point[0]]
        toc = time.perf_counter()
        logging.debug(f"Label2 time: {toc - tic:0.4f}s")
        logging.debug(f"Label2 size: {np.array(object=seed_label).shape}")

        tic = time.perf_counter()
        # Create a new mask with only the selected region
        new_mask = (labeled_array == seed_label)
        toc = time.perf_counter()
        logging.debug(f"New mask time: {toc - tic:0.4f}s")
        logging.debug(f"New mask size: {np.array(object=new_mask).shape}")

        tic = time.perf_counter()
        # Generate a new image, replacing the selected region color
        new_img_array: np.ndarray = self.image.copy()
        new_img_array[new_mask] = new_color
        toc = time.perf_counter()
        logging.debug(f"New image time: {toc - tic:0.4f}s")
        
        self.image = new_img_array

    def draw_legend(self) -> None:
        '''Draw legend of players and their colors on the map'''
        logging.debug(f"Creating and drawing legend")

        n = len(self.players)
        name_width: int = 0
        for _, player in self.players.items():
            if (len(player.name) > name_width):
                name_width = len(player.name)

        rows       = (n-1) +1
        cellHeight = 45
        cellWidth  = 45
        imgHeight  = cellHeight * rows
        imgWidth   = (cellWidth * 3) + (name_width * 11) 

        i = Image.new("RGB", (imgWidth, imgHeight), (0,0,0))
        a = ImageDraw.Draw(i)
        font = ImageFont.truetype(font=self.font_path.__str__(), size=14)

        for outer, playername in enumerate(self.players):
            player = self.players[playername]
            for inner, level in enumerate(self.levels):
                prev: int = 0
                if (inner > 0):
                    prev = inner * ((cellWidth * (outer % 1)) + cellWidth)

                x0: int = prev + cellWidth * (outer % 1)
                y0: int = cellHeight * (outer // 1)
                x1: int = x0 + cellWidth
                y1: int = y0 + cellHeight
                a.rectangle([x0, y0, x1, y1], fill=player.colors[level].rgb, outline='black')

                if (inner == len(self.levels) - 1):
                    a.text((x1+1, y0+10), player.name, fill='white', font=font)

        legend = np.array(object=i)
        self.image[-legend.shape[0]:, 0:legend.shape[1]] = legend