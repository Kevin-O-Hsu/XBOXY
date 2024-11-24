from flask import Flask, jsonify, request
from pem import CertificateGenerator
from encrypt import AsymmetricEncryption
from database import DatabaseManager
import json
import time

cert_gen = CertificateGenerator()
cert_gen.generate_certificate()

app = Flask(__name__)

@app.route('/api/verify', methods=['POST'])
def receive_data():
    data = request.get_json() 
    result = handle_request(data)
    return jsonify({"pass": result, "status": "success"})

def handle_request(data) -> bool:
    try:
        encryption = AsymmetricEncryption(public_key_path="cnk/public_key.pem", private_key_path="cnk/private_key.pem")
        encryption.load_private_key()

        # 解密license_key
        decrypted_data = encryption.decrypt(str(data["license_key"]))
        rdata = json.loads(decrypted_data)

        # 验证作者
        if rdata.get("author") != "GreshAnt":
            return False
        print(rdata)
        
        keydb = DatabaseManager("data/activation.db")

        # 确保数据库有 'expire' 列，只需要初始化时添加一次
        keydb.add_column("expire")
        keydb.add_column('hwid')
        
        print(1)
        
        # 获取或插入 license_key 和 hwid
        result = keydb.get_or_insert(str(data["license_key"]),"hwid" ,str(data["hwid"]))
        
        print(2)
        
        # 计算到期时间（expiretime_msonly_ms 为毫秒数）
        expire_time = keydb.get_or_insert(str(data["license_key"]), "expire", 
                                         (int(time.time() * 1000) + int(rdata['expiretime_msonly_ms'])))

        keydb.close()
        
        print(expire_time, result, int(time.time()*1000))

        print(3)
        # 验证 hwid 和 expire
        hwid_valid = validate_hwid(result, data["hwid"])
        expire_valid = validate_expiry(expire_time)

        return hwid_valid and expire_valid
    except Exception as e:
        print(f"Error: {e}")
        return False

def validate_hwid(result, hwid) -> bool:
    # 如果没有找到 key，则认为是新用户，默认为通过
    if not result[0]:
        return True
    # 否则比较 hwid 是否一致
    return result[1] == str(hwid)

def validate_expiry(expire_time) -> bool:
    # 如果没有设置过期时间，则认为是新用户，自动通过
    if not expire_time[0]:
        return True
    # 如果已经有设置的过期时间，验证当前时间是否小于到期时间
    return int(time.time() * 1000) < int(expire_time[1])


if __name__ == '__main__':
    '/etc/letsencrypt/live/lamic.top/fullchain.pem', '/etc/letsencrypt/live/lamic.top/privkey.pem'
    # app.run(host='0.0.0.0', port=8443, ssl_context=('cnk/cert.pem', 'cnk/key.pem'))
    app.run(host='0.0.0.0', port=8443, ssl_context=('/etc/letsencrypt/live/lamic.top/fullchain.pem', '/etc/letsencrypt/live/lamic.top/privkey.pem'))