#!/bin/sh

# Define the target directory and target file name
TARGET_DIRECTORY="/usr/local/bin"
TARGET_FILE="ye"

if cp ye.py "$TARGET_DIRECTORY/$TARGET_FILE"; then
	echo "Copied ye to $TARGET_DIRECTORY/$TARGET_FILE"
else
	echo "Failed to copy ye.py"
	exit 1
fi

if chmod +x "$TARGET_DIRECTORY/$TARGET_FILE"; then
	echo "Made $TARGET_DIRECTORY/$TARGET_FILE executable"
else
	echo "Failed to make $TARGET_DIRECTORY/$TARGET_FILE executable"
	exit 1
fi

echo "Installation complete. Test the program by running [ye help] "
