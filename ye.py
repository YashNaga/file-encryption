#!/usr/bin/env python3

import sys
import os
from cryptography.fernet import Fernet, InvalidToken


def generateFileKey(keyPath):
    with open(keyPath, "wb") as filekey:
        key = Fernet.generate_key()
        filekey.write(key)
    print(f"New key generated and saved to {keyPath}.")

def copyKey():
    specPath = input("Please specify the location of the existing key: ").strip()
    if os.path.exists(specPath) and os.path.isfile(specPath):
        with open(specPath, "rb") as filekey:
            key = filekey.read()
        with open(keyPath, "wb") as filekey:
            filekey.write(key)
        print(f"Key copied from {specPath} to {keyPath}.")
    else:
        print(f"No valid key file found at {specPath}.")

def keyCheck(keyPath):
    while True:
        choice = input("No key file found. Would you like to create a new key or specify the location of an existing key? (create/specify): ").strip().lower()
        if choice == "create":
            generateFileKey(keyPath)
            break
        elif choice == "specify":
            copyKey()
        else:
            print("Invalid choice. Please type 'create' or 'specify'.")

# Same as last keyPath, concat directory to keep filekey.key in the same dir as the main.py script
keyPath = os.path.join(os.path.dirname(__file__), ".ye_filekey.key")

try:
    with open(keyPath, "rb") as filekey:
        key = filekey.read()
except FileNotFoundError:
    # If file doesnt exist attempt key generation (which will generate a file if there isnt one)
    keyCheck(keyPath)
    with open(keyPath, "rb") as filekey:
        key = filekey.read()

fernet = Fernet(key)

# Check if all arguements are present
if len(sys.argv) < 2:
    print(f"Error: Missing arguements\nUsage: ye <method> <filename>")
    sys.exit(1)

# Terminal arguements
method = sys.argv[1]

if method == "cpkey":
    copyKey()
    sys.exit(0)
elif method == "help":
    print(f"Usage: ye <method> <filename>\n\nMethods include: 'encrypt', 'decrypt', 'cpkey','help'\nSecond arguements for the respective methods: <filename>, <filename>, <filekey_location>, <none>\n\nMake sure you dont delete your .ye_filekey.key wherever its located as this is the key used\nto encrypt and decrypt any of the files you use through this program,\ncpkey copies the key from the file you specify to the .ye_filekey.key so be careful using\nthis command as you may lose your original key and any encrypyted information with it.")
    sys.exit(0)

if len(sys.argv) < 3:
    print(f"Error: Missing arguements\nUsage: ye <method> <filename>")
    sys.exit(1)

file_path = sys.argv[2]


def decrypt(filename):
    try:
        with open(filename, "rb") as encryptedFile:
            # Store file content
            encrypted = encryptedFile.read()

        # Decrypt the stored content
        decrypted = fernet.decrypt(encrypted)

        with open(filename, "wb") as decryptedFile:
            # Write the decrypted content back into the file
            decryptedFile.write(decrypted)

        print("File successfully decrypted!")
    except FileNotFoundError:
        print("Error: The file you are trying to decrypt cannot be found")
        sys.exit(1)
    except InvalidToken:
        print("Error: The provided key is incorrect or the file is corrupted")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An error occured while decrypting the file. {str(e)}")
        sys.exit(1)


def encrypt(filename):
    try:
        with open(filename, "rb") as file:
            # Store file c ontent
            original = file.read()

        # Encrypt stored file content
        encrypted = fernet.encrypt(original)

        with open(filename, "wb") as encrypted_file:
            # Write encrypted content back into the file
            encrypted_file.write(encrypted)

        print("File successfully encrypted!")
    except FileNotFoundError:
        print("Error: the file you are trying to encrypt cannot be found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An error occured while encrypting the file. {str(e)}")
        sys.exit(1)


if method == "encrypt":
    encrypt(file_path)
elif method == "decrypt":
    decrypt(file_path)
else:
    print(f"Error: Invalid method arguement\nMethods available: [encrypt, decrypt]")
