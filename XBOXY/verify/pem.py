from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import os

class CertificateGenerator:
    def __init__(self, country_name="US", state_name="California", locality_name="San Francisco", 
                 organization_name="My Organization", common_name="localhost", 
                 cert_file="cnk/cert.pem", key_file="cnk/key.pem", key_size=2048, validity_days=365):
        # 确保目录存在
        os.makedirs(os.path.dirname(cert_file), exist_ok=True)
        
        self.country_name = country_name
        self.state_name = state_name
        self.locality_name = locality_name
        self.organization_name = organization_name
        self.common_name = common_name
        self.cert_file = cert_file
        self.key_file = key_file
        self.key_size = key_size
        self.validity_days = validity_days

    def generate_certificate(self):
        # Generate RSA private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )

        # Save the private key to a PEM file
        with open(self.key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Create certificate subject and issuer
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name),
        ])

        # Use timezone-aware datetimes for validity
        certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=self.validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(self.common_name)]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())

        # Save the certificate to a PEM file
        with open(self.cert_file, "wb") as f:
            f.write(certificate.public_bytes(serialization.Encoding.PEM))

        print(f"Certificate and key generated and saved as {self.cert_file} and {self.key_file}")

# 使用示例
if __name__ == "__main__":
    cert_gen = CertificateGenerator()
    cert_gen.generate_certificate()
