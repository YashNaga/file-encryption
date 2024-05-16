import sys
import os
from cryptography.fernet import Fernet


def generateFileKey():
    keyPath = os.path.join(os.path.dirname(__file__), "filekey.key")
    try:
        with open(keyPath, "wb") as filekey:
            fileSize = os.path.getsize("filekey.key")

            if fileSize == 0:
                key = Fernet.generate_key()
                filekey.write(key)
    except FileNotFoundError:
        with open("filekey.key", "wb") as filekey:
            pass
        generateFileKey()


keyPath = os.path.join(os.path.dirname(__file__), "filekey.key")
try:
    with open(keyPath, "rb") as filekey:
        key = filekey.read()
except FileNotFoundError:
    generateFileKey()
    with open(keyPath, "rb") as filekey:
        key = filekey.read()

fernet = Fernet(key)

method = sys.argv[1]
file_path = sys.argv[2]


def decrypt(filename):
    with open(filename, "rb") as encryptedFile:
        encrypted = encryptedFile.read()

    decrypted = fernet.decrypt(encrypted)

    with open(filename, "wb") as decryptedFile:
        decryptedFile.write(decrypted)


def encrypt(filename):
    with open(filename, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(encrypted)


if method == "encrypt":
    encrypt(file_path)
elif method == "decrypt":
    decrypt(file_path)
else:
    print("Missing an arguement")
