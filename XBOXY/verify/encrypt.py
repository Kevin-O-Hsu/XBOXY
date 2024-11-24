from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class AsymmetricEncryption:
    def __init__(self, public_key_path="public_key.pem", private_key_path="private_key.pem"):
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path
        self.public_key = None
        self.private_key = None
    
    def load_public_key(self):
        # 加载公钥，用于加密（客户端使用）
        with open(self.public_key_path, "rb") as public_key_file:
            self.public_key = serialization.load_pem_public_key(
                public_key_file.read()
            )

    def load_private_key(self):
        # 加载私钥，用于解密（服务器使用）
        with open(self.private_key_path, "rb") as private_key_file:
            self.private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None
            )

    def encrypt(self, message):
        if self.public_key is None:
            raise ValueError("Public key not loaded. Use load_public_key() to load it.")
        
        # 使用公钥加密
        ciphertext = self.public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode("ascii")

    def decrypt(self, ciphertext_base64):
        if self.private_key is None:
            raise ValueError("Private key not loaded. Use load_private_key() to load it.")
        
        # Base64 解码并解密
        ciphertext = base64.b64decode(ciphertext_base64)
        decrypted_message = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode("utf-8")

if __name__ == "__main__":
    encryption = AsymmetricEncryption(public_key_path="cnk/public_key.pem", private_key_path="cnk/private_key.pem")
    encryption.load_public_key()
    encryption.load_private_key()
    message = "Hello, World!"
    encrypted_message = encryption.encrypt(message)
    print("Encrypted Message:", encrypted_message)
    decrypted_message = encryption.decrypt(encrypted_message)
    print("Decrypted Message:", decrypted_message)