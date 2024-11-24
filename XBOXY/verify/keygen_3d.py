from encrypt import AsymmetricEncryption
import time
import json
import pyperclip
import random
import string

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # 包含大小写字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

activation_code = \
    {
        "gentime" : int(time.time() * 1000),
        "expiration" : int(time.time() * 1000)+259200000,
        "author" : "GreshAnt",
        "randompart" : generate_random_string(64)
    }
encryption = AsymmetricEncryption(public_key_path="cnk/public_key.pem", private_key_path="cnk/private_key.pem")
encryption.load_public_key()
r = encryption.encrypt(json.dumps(activation_code))
print("三天激活码已生成")
print(r)
pyperclip.copy(r)
