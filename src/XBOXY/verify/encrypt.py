from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class AsymmetricEncryption:
    
    
    def __init__(self, public_key_path="public_key.pem", private_key_path="private_key.pem") -> None:
        """
        The function initializes with default paths for public and private keys and sets them to None.
        
        :param public_key_path: The `public_key_path` parameter in the `__init__` method is a default
        parameter that is set to "public_key.pem" if no value is provided when creating an instance of the
        class. This parameter is used to specify the path to the public key file, defaults to public_key.pem
        (optional)
        :param private_key_path: The `private_key_path` parameter in the `__init__` method is a default
        parameter that is set to "private_key.pem" if no value is provided when creating an instance of the
        class. This parameter is used to specify the path to the private key file, defaults to
        private_key.pem (optional)
        """
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path
        self.public_key = None
        self.private_key = None
    
    def load_public_key(self) -> None:
        """
        The `load_public_key` function loads a public key from a specified file path for encryption purposes
        on the client side.
        """
        # 加载公钥，用于加密（客户端使用）
        with open(self.public_key_path, "rb") as public_key_file:
            self.public_key = serialization.load_pem_public_key(
                public_key_file.read()
            )

    def load_private_key(self) -> None:
        """
        The `load_private_key` function loads a private key from a file for decryption purposes on the
        server.
        """
        # 加载私钥，用于解密（服务器使用）
        with open(self.private_key_path, "rb") as private_key_file:
            self.private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None
            )

    def encrypt(self, message: str) -> str:
        """
        The `encrypt` function encrypts a message using a public key with OAEP padding and returns the
        ciphertext in base64 format.
        
        :param message: The `message` parameter in the `encrypt` method is the plaintext message that you
        want to encrypt using the public key. It should be a string representing the message that you want
        to keep confidential
        :return: The encrypt method returns the encrypted message in base64 encoded format.
        """
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

    def decrypt(self, ciphertext_base64: str) -> str:
        """
        The `decrypt` function takes a base64-encoded ciphertext, decodes and decrypts it using a private
        key, and returns the decrypted message as a UTF-8 encoded string.
        
        :param ciphertext_base64: The `ciphertext_base64` parameter is a base64 encoded string representing
        the encrypted message that you want to decrypt using the private key. This function first decodes
        the base64 string to obtain the ciphertext, then decrypts it using the private key loaded in the
        `self.private_key` attribute
        :return: The `decrypt` method returns the decrypted message in UTF-8 format.
        """
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
