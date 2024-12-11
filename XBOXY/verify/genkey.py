import time
from datetime import datetime
import json
import pyperclip
import random
import string
user_input = input("expiration YYYY-MM-DD HH:MM>")
dt = datetime.strptime(user_input, "%Y-%m-%d %H:%M")
timestamp = int(time.mktime(dt.timetuple())*1000)

from .encrypt import AsymmetricEncryption


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # 包含大小写字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
author = input("author>")
activation_code = \
    {
        "gentime" : int(time.time() * 1000),
        "expiration" : timestamp,
        "author" : author,
        "randompart" : generate_random_string(64)
    }
encryption = AsymmetricEncryption(public_key_path="cnk/public_key.pem", private_key_path="cnk/private_key.pem")
encryption.load_public_key()
r = encryption.encrypt(json.dumps(activation_code))
print(r)
pyperclip.copy(r)
