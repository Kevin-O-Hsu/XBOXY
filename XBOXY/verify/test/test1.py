from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# 假设已经加载了公钥和私钥，如前面的代码
# 加载公钥和私钥
with open("data/public_key.pem", "rb") as public_key_file:
    public_key = serialization.load_pem_public_key(
        public_key_file.read(),
    )

with open("cnk/private_key.pem", "rb") as private_key_file:
    private_key = serialization.load_pem_private_key(
        private_key_file.read(),
        password=None,
    )

# 要加密的消息
message = b"test"

# 使用公钥加密
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("加密后的数据：", ciphertext)

# 使用私钥解密
decrypted_message = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("解密后的数据：", decrypted_message.decode("utf-8"))
