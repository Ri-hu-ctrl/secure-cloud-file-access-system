from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# Load RSA private key
private_key = RSA.import_key(open("keys/private.pem").read())

cipher_rsa = PKCS1_OAEP.new(private_key)

# Load encrypted AES key
with open("storage/encrypted_key.bin","rb") as f:
    encrypted_key = f.read()

aes_key = cipher_rsa.decrypt(encrypted_key)

# Load encrypted file
with open("storage/encrypted_file.bin","rb") as f:
    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read()

cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)

data = cipher_aes.decrypt(ciphertext)

with open("decrypted_file.txt","wb") as f:
    f.write(data)

print("File Decrypted Successfully")