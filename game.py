#!/usr/bin/env python3
# External
import logging
from PIL import Image
import numpy as np
from scipy.ndimage import measurements
# Internal
from datatypes import (ColorBase, Color, LevelBase, Level, Player, Province, Region)
from data import Data

class Game:
    def __init__(self, file: Data) -> None:
        self.file: Data = file

    def fill(input_image_path: str, output_image_path: str, seed_point: list[int, int], new_color: set(int, int, int)):
        # Open image and convert to RGB
        image = Image.open(input_image_path).convert("RGB")

        # Convert image data to numpy array
        img_array = np.array(image)

        # Get color at the seed_point
        seed_color = img_array[seed_point[1], seed_point[0]]

        # Generate a binary image (mask) where pixels with the seed color are white
        mask = np.all(img_array == seed_color, axis=-1)

        # Label all connected regions in the mask
        labeled_array, num_features = measurements.label(mask)

        # Get label of the region where seed_point is located
        seed_label = labeled_array[seed_point[1], seed_point[0]]

        # Create a new mask with only the selected region
        new_mask = (labeled_array == seed_label)

        # Generate a new image, replacing the selected region color
        new_img_array = img_array.copy()
        new_img_array[new_mask] = new_color

        # Convert array to image
        new_image = Image.fromarray(np.uint8(new_img_array))

        # Save the output image
        new_image.save(output_image_path)