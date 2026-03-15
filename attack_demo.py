with open("storage/encrypted_file.bin","rb") as f:
    data = f.read()

print("Attacker trying to read encrypted file:\n")
print(data)