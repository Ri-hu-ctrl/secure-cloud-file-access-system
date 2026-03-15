from flask import Flask, render_template, request, redirect, send_file
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import hashlib
import os

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "1234"

UPLOAD_FOLDER = "uploads"
STORAGE_FOLDER = "storage"

# ---------------- LOGIN ----------------

@app.route('/', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        user = request.form['username']
        pwd = request.form['password']

        if user == USERNAME and pwd == PASSWORD:
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# ---------------- FILE UPLOAD + ENCRYPT ----------------

@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath,"rb") as f:
        data = f.read()

    # SHA256 hash
    hash_value = hashlib.sha256(data).hexdigest()

    # AES Encryption
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)

    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    # RSA Encryption of AES key
    public_key = RSA.import_key(open("keys/public.pem").read())
    cipher_rsa = PKCS1_OAEP.new(public_key)

    encrypted_key = cipher_rsa.encrypt(aes_key)

    # Save encrypted file
    with open("storage/encrypted_file.bin","wb") as f:
        f.write(cipher_aes.nonce)
        f.write(tag)
        f.write(ciphertext)

    with open("storage/encrypted_key.bin","wb") as f:
        f.write(encrypted_key)

    with open("storage/hash.txt","w") as f:
        f.write(hash_value)

    return "File Uploaded & Encrypted Successfully"

# ---------------- DOWNLOAD + DECRYPT ----------------

@app.route('/download')
def download():

    private_key = RSA.import_key(open("keys/private.pem").read())

    cipher_rsa = PKCS1_OAEP.new(private_key)

    with open("storage/encrypted_key.bin","rb") as f:
        encrypted_key = f.read()

    aes_key = cipher_rsa.decrypt(encrypted_key)

    with open("storage/encrypted_file.bin","rb") as f:

        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)

    data = cipher_aes.decrypt(ciphertext)

    with open("storage/decrypted_file.txt","wb") as f:
        f.write(data)

    return send_file("storage/decrypted_file.txt", as_attachment=True)

# ---------------- ATTACK DEMO ----------------

@app.route('/attack')
def attack():

    with open("storage/encrypted_file.bin","rb") as f:
        data = f.read()

    return render_template("attack.html",data=data)

# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)