# Internal
from app.core.color import ColorBase


class LevelBase:
    '''Container class for individual levels'''
    def __init__(self, name: str, cost: int, product: int, color: ColorBase):
        '''Container class for individual levels
        :name: Friendly level name
        :cost: Cost for a province at this level
        :product: How much a province at this level produces
        :color: Default color for a province at this level'''
        self.name: str = name
        self.cost: int = cost
        self.product: int = product
        self.color: ColorBase = color  
    
    def __repr__(self) -> str: return self.__str__() # Printable representation
    def __str__(self) -> str: return str(self.__dict__) # String representation