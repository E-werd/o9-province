#!/usr/bin/env python3
# External
import logging
from PIL import Image
import numpy as np
from scipy.ndimage import measurements
from pathlib import Path

class Map:
    def __init__(self, in_image: Path, out_image: Path = None) -> None:
        self.in_image_path: Path = in_image
        self.out_image_path: Path = out_image
        
        if (self.out_image_path == None):
            out_stem: str = "out_" + self.in_image_path.stem
            self.out_image_path = self.in_image_path.with_stem(stem=out_stem).resolve()

        logging.info(f"Loading map image from file: {self.in_image_path}")
        self.image: np.ndarray = self.__get_image_array(img_path=self.in_image_path)

    def __get_image_array(self, img_path: str) -> np.ndarray:
        # Open image and convert to RGB
        img = Image.open(fp=img_path, mode="r").convert("RGB") # Returns PIL.Image.Image object

        # Convert image data to numpy array
        img_array = np.array(object=img) # returns np.ndarray object, basically just an array
        return img_array

    def write(self, dest: Path = None) -> None:
        # Convert array to image
        new_image = Image.fromarray(obj=np.uint8(self.image))

        # Save the output image
        if (dest == None): 
            logging.debug(f"Writing map to {self.out_image_path.__str__()}")
            new_image.save(self.out_image_path.__str__())
        else: 
            logging.debug(f"Writing map to {dest.__str__()}")
            new_image.save(dest.__str__())

    def fill(self, seed_point: tuple, new_color: tuple) -> None:
        logging.debug(f"Filling province at {str(seed_point)} with color {str(new_color)}")
        # Get color at the seed_point
        seed_color = self.image[seed_point[1], seed_point[0]] # Gets pixel in rgb at image coords [y, x]

        # Generate a binary image (mask) where pixels with the seed color are white
        mask = np.all(self.image == seed_color, axis=-1)

        # Label all connected regions in the mask
        labeled_array, num_features = measurements.label(mask)

        # Get label of the region where seed_point is located
        seed_label = labeled_array[seed_point[1], seed_point[0]]

        # Create a new mask with only the selected region
        new_mask = (labeled_array == seed_label)

        # Generate a new image, replacing the selected region color
        new_img_array: np.ndarray = self.image.copy()
        new_img_array[new_mask] = new_color
        
        self.image = new_img_array