#!/usr/bin/env python3

import sys
import os
from cryptography.fernet import Fernet, InvalidToken


def generateFileKey():
    # Get current path and concat with filekey.key
    keyPath = os.path.join(os.path.dirname(__file__), ".filekey.key")
    try:
        with open(keyPath, "wb") as filekey:
            # Check file size
            fileSize = os.path.getsize(".filekey.key")

            if fileSize == 0:
                # If file is empty generate a key and write to it
                key = Fernet.generate_key()
                filekey.write(key)
    except FileNotFoundError:
        # If file doesnt exist generate the file and attempt to generate the key again
        with open(".filekey.key", "wb") as filekey:
            pass
        generateFileKey()


# Same as last keyPath, concat directory to keep filekey.key in the same dir as the main.py script
keyPath = os.path.join(os.path.dirname(__file__), ".filekey.key")
try:
    with open(keyPath, "rb") as filekey:
        key = filekey.read()
except FileNotFoundError:
    # If file doesnt exist attempt key generation (which will generate a file if there isnt one)
    generateFileKey()
    with open(keyPath, "rb") as filekey:
        key = filekey.read()

fernet = Fernet(key)

# Check if all arguements are present
if len(sys.argv) < 3:
    print(f"Error: Missing arguements\nUsage: ye <method> <filename>")
    sys.exit(1)

# Terminal arguements
method = sys.argv[1]
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
            # Store file content
            original = file.read()

        # Encrypt stored file content
        encrypted = fernet.encrypt(original)

        with open(filename, "wb") as encrypted_file:
            # Write encrypted content back into the file
            encrypted_file.write(encrypted)
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
