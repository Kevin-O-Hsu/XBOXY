import sqlite3
import os


class DatabaseManager:
    def __init__(self, db_name="data/activation.db"):
        """
        The function initializes a database connection and creates a table if it doesn't exist.
        
        :param db_name: The `db_name` parameter is a string that represents the path to the SQLite database
        file. In the `__init__` method of the class, it is used to initialize the database connection by
        creating the database file if it doesn't exist and connecting to it using SQLite, defaults to
        data/activation.db (optional)
        """
        self.db_name = db_name
        # 检查并创建目录
        os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """
        The `_create_table` function creates a table named `key_value_store` with columns for key and value
        if it does not already exist.
        """
        # 创建用于存储键值对的表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS key_value_store (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.connection.commit()

    def get_or_insert(self, key, column_name, value=None):
        """
        The `get_or_insert` function checks if a key exists in a key-value store, retrieves or inserts a
        value for a specified column associated with the key, and returns the value along with a boolean
        indicating if the value was retrieved or inserted.
        
        :param key: The `key` parameter is used as a unique identifier for the key-value pair in the
        `key_value_store` table. It is used to look up and manipulate the corresponding data associated with
        that key
        :param column_name: The `column_name` parameter in the `get_or_insert` method refers to the name of
        the column in the database table `key_value_store` where you want to store or retrieve the value
        associated with a specific key. This parameter is used to specify which column to interact with when
        getting or inserting
        :param value: The `value` parameter in the `get_or_insert` method represents the value that you want
        to insert or update in the database for a given key and column. If the key already exists in the
        database, the method will either return the existing value for the specified column or update it
        with the new
        :return: The `get_or_insert` method returns a tuple containing two values. The first value is a
        boolean indicating whether the operation was an insertion (True) or an update (False). The second
        value is the actual value retrieved or inserted into the specified column for the given key.
        """
        # 先检查 key 是否存在
        self.cursor.execute("SELECT value FROM key_value_store WHERE key = ?", (key,))
        result = self.cursor.fetchone()

        if result:
            # 如果 key 存在，查询并返回该列的值
            # 检查该列是否有值
            self.cursor.execute(f"SELECT {column_name} FROM key_value_store WHERE key = ?", (key,))
            column_result = self.cursor.fetchone()
            if column_result and column_result[0]:
                # 如果列已经有值，返回它
                return True, column_result[0]
            else:
                # 如果列为空，插入新值
                if value is not None:
                    self.add_column(column_name)  # 确保该列存在
                    self.cursor.execute(f"UPDATE key_value_store SET {column_name} = ? WHERE key = ?", (value, key))
                    self.connection.commit()
                    return False, value
                else:
                    return False, None  # 如果没有提供默认值
        else:
            # 如果 key 不存在，插入新键值对并插入新列的值
            self.cursor.execute("INSERT INTO key_value_store (key, value) VALUES (?, ?)", (key, value))
            self.connection.commit()

            # 插入新列并设置其值
            if value is not None:
                self.add_column(column_name)  # 确保该列存在
                self.cursor.execute(f"UPDATE key_value_store SET {column_name} = ? WHERE key = ?", (value, key))
                self.connection.commit()
            return False, value
        
    def get_all_records(self):
        """
        The function `get_all_records` retrieves all records from a table named `key_value_store`.
        :return: A list of all records from the "key_value_store" table is being returned.
        """
        # 获取表中所有记录
        self.cursor.execute("SELECT * FROM key_value_store")
        return self.cursor.fetchall()

    def add_column(self, column_name, column_type="TEXT"):
        """
        The `add_column` function in Python checks if a column exists in a SQLite table and adds it if it
        doesn't.
        
        :param column_name: The `column_name` parameter in the `add_column` method represents the name of
        the column that you want to add to a table in a SQLite database. It is a required parameter for this
        method. When calling the `add_column` method, you need to provide the name of the column you
        :param column_type: The `column_type` parameter in the `add_column` method specifies the data type
        for the new column being added to the table. By default, if the `column_type` parameter is not
        provided when calling the `add_column` method, the data type for the new column will be set to,
        defaults to TEXT (optional)
        """
        try:
            # 查询表的列信息，检查列是否已存在
            self.cursor.execute(f"PRAGMA table_info(key_value_store)")
            columns = [column[1] for column in self.cursor.fetchall()]  # 获取所有列名

            if column_name in columns:
                print(f"Column '{column_name}' already exists.")
            else:
                # 如果列不存在，添加该列
                self.cursor.execute(f"ALTER TABLE key_value_store ADD COLUMN {column_name} {column_type}")
                self.connection.commit()
                print(f"Column '{column_name}' added successfully.")
        except sqlite3.OperationalError as e:
            print(f"Error adding column '{column_name}': {e}")
    
    

    def close(self):
        """
        The `close` function closes the database connection.
        """
        # 关闭数据库连接
        self.connection.close()
