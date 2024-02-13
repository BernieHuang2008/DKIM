from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load the public key
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Convert the public key to the OpenSSH format
public_key_openssh = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

# Remove the "ssh-rsa " at the beginning and the key comment at the end
public_key_dns = public_key_openssh.split()[1]

# Print the DKIM DNS record
print('v=DKIM1; k=rsa; p={}'.format(public_key_dns.decode()))