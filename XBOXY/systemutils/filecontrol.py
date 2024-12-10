import pathlib
import orjson
import os
import sys
from XBOXY.log import logger

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
        return self.path.exists()
    
    def create_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        logger.info(f"创建文件: {self.path}")
        return self
    
    

class JsonFile(File):
    def __init__(self, path: pathlib.Path, needed: bool = False):
        super().__init__(path, needed)

    def exists(self):
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
        if not isinstance(data, (dict, list)):
            raise ValueError("只能写入字典或列表类型的JSON数据")
        self.path.write_text(orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8"))
        logger.info(f"写入JSON文件: {self.path}")
        return self

    # 操作字典数据
    def update_json_data(self, knv: tuple[object, object]):
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
