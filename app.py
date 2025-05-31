import string
import random
from cryptography.fernet import Fernet



def generate_password():
    password = random.choices(string.ascii_letters+string.digits+string.punctuation, k=13)
    return "".join(password)

def encrypt_password(password):
    key = Fernet.generate_key()
    with open("key.key", 'wb') as f:
        f.write(key)
    fi = Fernet(key)
    cipher_text = fi.encrypt(password)
    return cipher_text

def decrypt_password(cipher_text):
    with open("key.key", 'r') as f:
        key = f.read()
    fi = Fernet(key)
    plain_text = fi.decrypt(cipher_text)
    return plain_text.decode('utf-8')


cipher  = encrypt_password(generate_password().encode('utf-8'))

print("Encrypted Password:", cipher)
plain = decrypt_password(cipher)
print("Decrypted Password:", plain)