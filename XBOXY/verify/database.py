import sqlite3
import os


class DatabaseManager:
    def __init__(self, db_name="data/activation.db"):
        self.db_name = db_name
        # 检查并创建目录
        os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        # 创建用于存储键值对的表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS key_value_store (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.connection.commit()

    def get_or_insert(self, key, column_name, value=None):
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
        # 获取表中所有记录
        self.cursor.execute("SELECT * FROM key_value_store")
        return self.cursor.fetchall()

    def add_column(self, column_name, column_type="TEXT"):
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
        # 关闭数据库连接
        self.connection.close()
