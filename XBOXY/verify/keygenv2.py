from encrypt import AsymmetricEncryption
import json
import pyperclip
import random
import string
import re


def convert_to_milliseconds(time_str):
    # 正则表达式匹配多个单位
    match = re.findall(r"(\d+)([smhd])", time_str.strip().lower())
    
    if not match:
        raise ValueError("Invalid time format. Please use s (seconds), m (minutes), h (hours), or d (days).")
    
    total_milliseconds = 0
    
    # 遍历匹配到的时间值和单位
    for value, unit in match:
        value = int(value)
        
        # 根据单位转换为毫秒
        if unit == 's':
            total_milliseconds += value * 1000  # 秒转毫秒
        elif unit == 'm':
            total_milliseconds += value * 1000 * 60  # 分钟转毫秒
        elif unit == 'h':
            total_milliseconds += value * 1000 * 60 * 60  # 小时转毫秒
        elif unit == 'd':
            total_milliseconds += value * 1000 * 60 * 60 * 24  # 天转毫秒

    return total_milliseconds

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # 包含大小写字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
# activation_code = \
#     {
#         "expiretime_msonly_ms" : convert_to_milliseconds(input("expiretime_msonly_ms>")),
#         "author" : "GreshAnt",
#         "randompart" : generate_random_string(64)
#     }
# encryption = AsymmetricEncryption(public_key_path="cnk/public_key.pem", private_key_path="cnk/private_key.pem")
# encryption.load_public_key()
# r = encryption.encrypt(json.dumps(activation_code))
# print(r)
# pyperclip.copy(r)

all_str = ''

for _ in range(1):
    
    activation_code = \
        {
            "expiretime_msonly_ms" : convert_to_milliseconds("7d"),
            "author" : "GreshAnt",
            "randompart" : generate_random_string(64)
        }
    encryption = AsymmetricEncryption(public_key_path="cnk/public_key.pem", private_key_path="cnk/private_key.pem")
    encryption.load_public_key()
    r = encryption.encrypt(json.dumps(activation_code))
    all_str += r + '\n'
print(all_str)
pyperclip.copy(all_str)