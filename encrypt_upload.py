from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import hashlib

file_path = input("Enter file name to upload: ")

with open(file_path, "rb") as f:
    data = f.read()

# SHA256 Hash
hash_value = hashlib.sha256(data).hexdigest()

# AES Key
aes_key = get_random_bytes(16)

cipher_aes = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)

# Load RSA Public Key
public_key = RSA.import_key(open("keys/public.pem").read())

cipher_rsa = PKCS1_OAEP.new(public_key)

encrypted_key = cipher_rsa.encrypt(aes_key)

# Save encrypted file
with open("storage/encrypted_file.bin","wb") as f:
    f.write(cipher_aes.nonce)
    f.write(tag)
    f.write(ciphertext)

# Save encrypted AES key
with open("storage/encrypted_key.bin","wb") as f:
    f.write(encrypted_key)

# Save hash
with open("storage/hash.txt","w") as f:
    f.write(hash_value)

print("File Encrypted and Uploaded Successfully")