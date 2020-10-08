from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

print('File to Encrypt: ', end=' ')
file_name = input()

if not os.path.exists(file_name):
    print('File Does not exist')
    exit()

data = None
with open(file_name, 'rb') as fs:
    data = fs.read()

print('Enter Key: ', end=' ')
key = input().encode()


def encrypt(data, cipher):
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return ciphertext

with open(file_name + '.encrypted', 'wb') as fs:
    key = pad(key, 16)[:16]
    cipher = AES.new(key, AES.MODE_CBC)
    fs.write(cipher.iv)
    fs.write(encrypt(data, cipher))

print('Encryption Done')