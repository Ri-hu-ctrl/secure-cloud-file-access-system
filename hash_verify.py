import hashlib

with open("decrypted_file.txt","rb") as f:
    data = f.read()

new_hash = hashlib.sha256(data).hexdigest()

with open("storage/hash.txt","r") as f:
    original_hash = f.read()

if new_hash == original_hash:
    print("File Integrity Verified")
else:
    print("File has been tampered!")