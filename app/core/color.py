# External
import logging
from PIL import ImageColor


class ColorBase:
    '''Container class for individual colors'''
    def __init__(self, name: str, rgb: tuple) -> None:
        '''Container class for individual colors
        :name: Friendly name for color
        :rgb: 3-element tuple (r, g, b) for color'''
        self.name: str = name
        self.rgb: tuple = rgb
        logging.debug(f"Generated color: {self.name} - {str(self.rgb)}")
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation

class Color:
    '''Static class for colors, provides colors by name from PIL'''
    @staticmethod
    def get_colors() -> dict[str, ColorBase]:
        all_colors: dict = ImageColor.colormap.items() # Get list of colors from PIL
        converted: dict[str, ColorBase] = {} # Declare, initialize dict

        def hex_to_rgb(hex: str) -> tuple:
            '''Convert color hex to rgb. Returns tuple'''
            h = hex.lstrip('#') # Remove pound
            return tuple(int(h[i:i+2], base=16) for i in (0, 2, 4)) # Convert each group of 2 from hexadecimal to base16

        for color in all_colors: # Loop through list of colors
            converted.update({color[0]: ColorBase(name=color[0], rgb=hex_to_rgb(color[1]))}) # Create color object, add to dict

        return converted # Return dict
    
    list: dict[str, ColorBase] = get_colors()
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation