from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from tkinter import *
from tkinter import filedialog
import os

global filename
button_height = 2
button_width = 25

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Use a 256-bit key
        salt=salt,
        iterations=100000,  # Adjust the number of iterations as needed for your security requirements
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def browseFiles():
    browseFiles.filename = filedialog.askopenfilename(initialdir="/", title="Select a File",)
    label_file_explorer.configure(text="File Selected: " + browseFiles.filename)

    pass_label.pack()
    password.pack()
    temp_label.pack()
    button_encrypt.pack()
    button_decrypt.pack()

def encrypt_file(password):
    #print(password)
    with open('aliceKey.txt', 'w') as file:
        file.write(password)
    with open(browseFiles.filename, 'rb') as file:
        original = file.read()

    salt = os.urandom(16)  # Generate a random salt
    key = derive_key(password, salt)
    backend = default_backend()
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)

    encryptor = cipher.encryptor()
    encrypted = encryptor.update(original) + encryptor.finalize()

    with open(browseFiles.filename, 'wb') as file:
        file.write(salt + iv + encrypted)  # Overwrite the original file with encrypted data

    status_label.configure(text="Encrypted", fg="green")
    status_label.pack()

def decrypt_file(password):
    with open(browseFiles.filename, 'rb') as file:
        data = file.read()
        salt = data[:16]  # Extract the salt used in encryption
        iv = data[16:32]  # Extract the IV used in encryption
        encrypted = data[32:]  # Extract the encrypted data

    key = derive_key(password, salt)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)

    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()

    with open(browseFiles.filename, 'wb') as file:
        file.write(decrypted)  # Overwrite the encrypted file with decrypted data

    status_label.configure(text="Decrypted", fg="green")
    status_label.pack()

window = Tk()

window.title('File Encryptor and Decryptor')
window.geometry("940x740")
window.config(background="black")

main_title = Label(window, text="File Encryptor and Decryptor", width=100, height=2, fg="white", bg="black", font=("", 30))
passwd = StringVar()

credit = Label(window, text="Cryptography(22CS5PCCRP) AAT by Amrutha Muralidhar and Ananya Aithal", bg="black", height=2,
               fg="white", font=("", 20))
label_file_explorer = Label(window, text="Select a File : ", width=100, height=2, fg="white", bg="black", font=("", 20))
pass_label = Label(window, text="Password for encryption/decryption : ", width=100, height=2, fg="white", bg="black",
                   font=("", 20))
temp_label = Label(window, text="", height=3, bg="black")

button_explore = Button(window, text="Browse File", command=browseFiles, width=button_width, height=button_height,
                        font=("", 17), bg="#61C0BF", fg="white")

password = Entry(window, textvariable=passwd, show="*")

button_encrypt = Button(window, text="Encrypt", command=lambda: encrypt_file(passwd.get()), width=button_width, height=button_height,
                        font=("", 17), bg="#61C0BF", fg="white")
button_decrypt = Button(window, text="Decrypt", command=lambda: decrypt_file(passwd.get()), width=button_width, height=button_height,
                        font=("", 17), bg="#61C0BF", fg="white")

status_label = Label(window, text="", width=100, height=4, fg="white", bg="black", font=("", 17))

credit.pack()
main_title.pack()
label_file_explorer.pack()
button_explore.pack()
window.mainloop()
