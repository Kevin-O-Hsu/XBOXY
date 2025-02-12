import pathlib
from typing import Literal
import orjson

from .. import log
logger = log.logger


class File(object):
    
    def __init__(self, path: pathlib.Path):
        """
        The function initializes an object with a given path and creates a file if it does not exist.
        
        :param path: The `path` parameter in the `__init__` method is expected to be a `pathlib.Path` object
        representing the file path. If a string is provided instead of a `pathlib.Path` object, it will be
        converted to a `pathlib.Path` object. If the provided
        :type path: pathlib.Path
        """
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            self.path = path
        else:
            raise TypeError("路径参数类型错误！")
        
        if not self.exists():
            self._create_file()

    def exists(self):
        """
        The `exists` function checks if a specified path exists.
        :return: The `exists` method is returning whether the path exists or not. It is checking if the file
        or directory at the specified path exists and returning a boolean value (True if it exists, False if
        it does not).
        """
        return self.path.exists()
    
    def _create_file(self):
        """
        The `create_file` function creates a file at a specified path and logs the action.
        :return: The `self` object is being returned.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        logger.info(f"创建文件: {self.path}")
        return self
    
    def del_file(self):
        """
        The function deletes a file if it exists.
        :return: The `self` object is being returned.
        """
        if self.exists():
            self.path.unlink()
            logger.info(f"删除文件: {self.path}")
        return self
    
    

class JsonFile(File):
    def __init__(self, path: pathlib.Path, type: Literal["dict", "list"]="dict"):
        """
        This Python function initializes an object with a specified path and type, defaulting to "dict" if
        not specified.
        
        :param path: The `path` parameter is of type `pathlib.Path` and represents the file path that will
        be used in the initialization of the class
        :type path: pathlib.Path
        :param type: The `type` parameter in the `__init__` method is a string literal that specifies the
        type of data structure to be used. It can be either "dict" for a dictionary or "list" for a list.
        The default value for this parameter is "dict" if no value is, defaults to dict
        :type type: Literal["dict", "list"] (optional)
        """
        super().__init__(path)
        self.type = type
        
        if not self.get_json_data():
            if self.type == "dict":
                data = {}
            else:
                data = []
        
            self.write_json_data(data)
    
    def get_json_data(self):
        """
        The `get_json_data` function reads JSON data from a file, handles errors, and returns the data as a
        dictionary or list based on a specified parameter.
        :return: The `get_json_data` method returns the JSON data loaded from a file using the `orjson`
        library. If the loaded data is not a dictionary or a list, a `ValueError` is raised. If there is an
        error during JSON decoding or if the data is not a dictionary or list and the `if_list` parameter is
        `False`, an empty dictionary is written to the file
        """
        try:
            data = orjson.loads(self.path.read_text())
            assert isinstance(data, (dict, list))
            if isinstance(data, dict):
                self.type = "dict"
            elif isinstance(data, list):
                self.type = 'list'
            
        except (orjson.JSONDecodeError, AssertionError):
            if self.type == "dict":
                data = {}
            else:
                data = []
        
            self.write_json_data(data)
        return data
        
    def write_json_data(self, data: list | dict):
        """
        This Python function writes JSON data (either a dictionary or a list) to a file with indentation and
        logs the action.
        
        :param data: The `data` parameter in the `write_json_data` method is expected to be a dictionary or
        a list containing the JSON data that you want to write to a file. If the `data` parameter is not a
        dictionary or a list, a `ValueError` will be raised with the message
        :return: The `self` object is being returned after writing the JSON data to the file.
        """
        assert isinstance(data, (dict, list))
        self.path.write_text(orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8"))
        logger.info(f"写入JSON文件: {self.path}")
        return self
    
    def append(self, value: tuple[object, object] | object):
        """
        The `append` function appends a tuple or object to a list or adds a key-value pair to a dictionary
        based on the type specified.
        
        :param value: The `value` parameter in the `append` method can be either a tuple containing two
        objects (`tuple[object, object]`) or a single object
        :type value: tuple[object, object] | object
        """
        data = self.get_json_data()
        match self.type:
            case "list":
                data.append(value)
            case "dict":
                data[value[0]] = value[1]
        self.write_json_data(data)
        return self

    def __getitem__(self, index: frozenset):
        data = self.get_json_data()
        return data[index]

    def __setitem__(self, index: frozenset, value):
        data = self.get_json_data()
        data[index] = value
        self.write_json_data(data)
        return self

    def __delitem__(self, index: frozenset):
        data = self.get_json_data()
        del data[index]
        self.write_json_data(data)
        return self

    def __len__(self):
        data = self.get_json_data()
        return len(data)

    def __iter__(self):
        data = self.get_json_data()
        match self.type:
            case "list":
                yield data
            case "dict":
                yield data.items()

    def __repr__(self):
        return repr(self.get_json_data())
