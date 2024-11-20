# External
import json, logging
import numpy as np
from pathlib import Path

class Data:
    '''Class for accessing and manipulating data'''
    class Source:
        '''Container class for data sources. Use 'types' for iteration.'''
        class Type:
            '''Container class for individual data sources'''
            def __init__(self, name: str, full: str, ext: str) -> None:
                self.name: str = name
                self.full: str = full
                self.ext: str = ext
        json: Type = Type(name="json", full="json data", ext=".json")
        npz: Type = Type(name="npz", full="NumPy data archive", ext=".npz")
        types: dict[str, Type] = {"json": json}

    def __init__(self, file: Path, source: Source.Type = Source.json) -> None:
        '''Class for accessing and manipulating data
        :file: File path for data source
        :source: Data source object. Data.Source.Type object, enumated in Data.Source.sources'''
        self.path: Path = file
        self.source: Data.Source.Type = source
        self.data: dict = self.__load_data(path=self.path.__str__())

    def __load_data(self, path: str) -> dict:
        '''Wraps buffering of data from any source into self.data'''
        match self.source:
            case Data.Source.json:
                return self.__load_json(path=path)
            case Data.Source.npz:
                return self.__load_npz(path=path)
            case _: return {} # This should never happen. Update loop with new data sources.

    def __load_json(self, path: str) -> dict:
        '''Buffers json from self.path into self.data'''
        try:
            logging.info(f"Loading data from file: {self.path.__str__()}")
            with open(file=path, mode="r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"*** File load error: {str(e)}")
            logging.warning(f"Assuming file is empty or missing, returning empty dataset.")
            return {}
        
    def __load_npz(self, path: str) -> dict:
        '''Buffers NumPy data from self.path into self.data'''
        try:
            logging.info(f"Loading data from file: {self.path.__str__()}")
            return np.load(file=path)
        except Exception as e:
            logging.error(f"*** File load error: {str(e)}")
            logging.warning(f"Assuming file is empty or missing, returning empty dataset.")
            return {}

    def __write_json(self) -> None:
        '''Writes json to self.path from self.data'''
        try:
            logging.info(f"Writing data to file: {self.path.__str__()}")
            with open(file=self.path.__str__(), mode='w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"*** File write error: {str(e)}")

    def __write_npz(self) -> None:
        '''Writes NumPy data to self.path from self.data'''
        try:
            logging.info(f"Writing data to file: {self.path.__str__()}")
            np.savez(file=self.path, **self.data)
        except Exception as e:
            logging.error(f"*** File write error: {str(e)}")

    def load_data(self, path: str) -> dict:
        '''Load from data source to buffer'''
        self.__load_data(path=path)

    def write_data(self) -> None:
        '''Write buffer to data source'''
        match self.source:
            case Data.Source.json: self.__write_json()
            case Data.Source.npz: self.__write_npz()
            case _: return # This should never happen. Update loop with new data sources.