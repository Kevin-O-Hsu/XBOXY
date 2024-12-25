# The class defines a File object and a JsonFile object for handling file operations, including
# creation, reading, writing, and manipulation of JSON data.
import pathlib
import orjson
import os
import sys

from .. import log
logger = log.logger


class File(object):
    
    def __init__(self, path: pathlib.Path, needed: bool = False):
        """
        Initialize a File object with a given path.

        If the script is compiled with Nuitka and the 'needed' flag is False, 
        the path is adjusted to point to the directory containing the executable.

        Args:
            path (pathlib.Path): The path of the file.
            needed (bool, optional): A flag indicating if the path adjustment 
                                    for Nuitka is necessary. Defaults to False.
        """
        if self.is_nuitka() and not needed:
            self.path = pathlib.Path(sys.executable).parent / path
        else:
            self.path = path
            
        self.is_exist = self.exists()
        
    def is_nuitka(self) -> bool:
        """
        Check if the script is compiled with Nuitka.
        """
        is_nuitka = "__compiled__" in globals()
        is_nuitka2 = "NUITKA_ONEFILE_PARENT" in os.environ
        return is_nuitka or is_nuitka2

    def exists(self):
        """
        The `exists` function checks if a specified path exists.
        :return: The `exists` method is returning whether the path exists or not. It is checking if the file
        or directory at the specified path exists and returning a boolean value (True if it exists, False if
        it does not).
        """
        return self.path.exists()
    
    def create_file(self):
        """
        The `create_file` function creates a file at a specified path and logs the action.
        :return: The `self` object is being returned.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        logger.info(f"创建文件: {self.path}")
        return self
    
    

class JsonFile(File):
    def __init__(self, path: pathlib.Path, needed: bool = False):
        """
        The function is a constructor that initializes an object with a given path and a boolean flag
        indicating if the path is needed.
        
        :param path: The `path` parameter is of type `pathlib.Path` and represents the file path that will
        be used in the initialization of the class
        :type path: pathlib.Path
        :param needed: The `needed` parameter in the `__init__` method is a boolean parameter with a default
        value of `False`. This means that if the `needed` parameter is not provided when creating an
        instance of the class, it will default to `False`, defaults to False
        :type needed: bool (optional)
        """
        super().__init__(path, needed)

    def exists(self):
        """
        The `exists` function checks if a specified path exists.
        :return: The `exists` method is returning whether the path exists or not. It is checking if the file
        or directory at the specified path exists and returning a boolean value (True if it exists, False if
        it does not).
        """
        return self.path.exists()

    def create_file(self):
        """
        Create the JSON file, if not exist.

        If the parent directory of the file does not exist, it will be created.

        Returns:
            self
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        logger.info(f"创建JSON文件: {self.path}")
        return self

    def get_json_data(self, if_list: bool=False):
        """
        The function `get_json_data` reads JSON data from a file, handles errors, and returns the data as a
        dictionary or list based on a specified parameter.
        
        :param if_list: The `if_list` parameter in the `get_json_data` method is a boolean parameter with a
        default value of `False`. This parameter is used to determine the behavior of the method when the
        loaded JSON data is neither a dictionary nor a list, defaults to False
        :type if_list: bool (optional)
        :return: The `get_json_data` method returns the JSON data loaded from a file using the `orjson`
        library. If the loaded data is not a dictionary or a list, a `ValueError` is raised. If there is an
        error during JSON decoding or if the data is not a dictionary or list and the `if_list` parameter is
        `False`, an empty dictionary is written to the file
        """
        try:
            data = orjson.loads(self.path.read_text())
            if not isinstance(data, (dict, list)):
                raise ValueError("JSON数据既不是字典也不是列表类型")
        except (orjson.JSONDecodeError, ValueError):
            if not if_list:
                self.write_json_data({})
                data = {}
            else:
                self.write_json_data([])
                data = []
        return data

    def write_json_data(self, data):
        """
        This Python function writes JSON data (either a dictionary or a list) to a file with indentation and
        logs the action.
        
        :param data: The `data` parameter in the `write_json_data` method is expected to be a dictionary or
        a list containing the JSON data that you want to write to a file. If the `data` parameter is not a
        dictionary or a list, a `ValueError` will be raised with the message
        :return: The `self` object is being returned after writing the JSON data to the file.
        """
        if not isinstance(data, (dict, list)):
            raise ValueError("只能写入字典或列表类型的JSON数据")
        self.path.write_text(orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8"))
        logger.info(f"写入JSON文件: {self.path}")
        return self

    # 操作字典数据
    def update_json_data(self, knv: tuple[object, object]):
        """
        This Python function updates or appends key-value pairs to JSON data for dictionaries.
        
        :param knv: The `knv` parameter in the `update_json_data` method is a tuple containing two objects.
        The first object in the tuple is the key, and the second object is the value that you want to update
        or append to the JSON data
        :type knv: tuple[object, object]
        :return: The `self` object is being returned after updating or appending the key-value pair to the
        JSON data.
        """
        """更新或追加键值对到JSON数据中，针对字典"""
        data = self.get_json_data()
        if not isinstance(data, dict):
            raise TypeError("JSON数据不是字典类型，无法更新键值对")
        data[knv[0]] = knv[1]
        self.write_json_data(data)
        logger.info(f"追加JSON数据: {self.path}")
        return self

    # 操作列表数据
    def append(self, value):
        """
        This Python function appends a value to a JSON data list and logs the action.
        
        :param value: The `value` parameter in the `append` method represents the data that you want to add
        to the JSON data as a new element in the list. It could be any valid Python data type such as a
        string, integer, float, list, dictionary, etc. When you call the `append
        :return: The `self` object is being returned.
        """
        """追加数据到JSON数据中，针对列表"""
        data = self.get_json_data(if_list=True)
        if not isinstance(data, list):
            raise TypeError("JSON数据不是列表类型，无法追加数据")
        data.append(value)
        self.write_json_data(data)
        logger.info(f"追加数据到JSON文件: {value}")
        return self

    def __getitem__(self, index):
        data = self.get_json_data()
        if isinstance(data, list):
            return data[index]
        elif isinstance(data, dict):
            return list(data.items())[index]
        else:
            raise TypeError("JSON数据既不是列表也不是字典")

    def __setitem__(self, index, value):
        data = self.get_json_data(if_list=True)
        if isinstance(data, list):
            data[index] = value
        else:
            raise TypeError("只能在列表类型的JSON数据中使用索引设置值")
        self.write_json_data(data)

    def __delitem__(self, index):
        data = self.get_json_data(if_list=True)
        if isinstance(data, list):
            del data[index]
        else:
            raise TypeError("只能在列表类型的JSON数据中删除值")
        self.write_json_data(data)

    def __len__(self):
        data = self.get_json_data()
        return len(data)

    def __iter__(self):
        data = self.get_json_data()
        if isinstance(data, list):
            return iter(data)
        elif isinstance(data, dict):
            return iter(data.items())
        else:
            raise TypeError("JSON数据既不是列表也不是字典")

    def __repr__(self):
        return repr(self.get_json_data())
