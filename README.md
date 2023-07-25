Encrypted and Compressed File Search System
This is a Python desktop program with a Tkinter interface that allows the user to load, compress, encrypt, and store files with an associated description. The user can also search for files using their description, which are then decrypted, decompressed, and saved to a chosen location.

Features
Load File: The user can select a file from their system to be loaded. The file is then compressed using the zlib library and encrypted using the cryptography library. The file's description is input by the user.

Search: The user can search for stored files by inputting the associated description. The program searches in the SQLite database for an exact match of the description.

Save File: If a file matching the search description is found, the user can choose a location to save the file. The file is then decrypted and decompressed before being saved.

How to Use
Run the Python file in the terminal or your IDE of choice.

In the graphical interface that appears, use the input field at the top to input the description of the file you want to load.

Click on the "Load File" button and select the file you want to load.

The file will be compressed, encrypted, and stored with the description you provided.

To search for a file, input the exact description into the second input field and click on "Search".

If a matching file is found, its description will be displayed. You can then click on "Save File" to save the decrypted and decompressed file to a location of your choice.

Dependencies
This program utilizes the following Python libraries:

tkinter
sqlite3
cryptography
os
zlib
Notes
This program creates an encryption key and stores it in 'key.key'. If this key is lost, the encrypted files will no longer be decryptable.

Files are stored in an SQLite database named 'files.db'. The files table contains two columns: 'description' (the user-provided description for each file) and 'file' (the compressed and encrypted file).

Warning
This program was created for educational purposes and should not be used to store sensitive or confidential information.
