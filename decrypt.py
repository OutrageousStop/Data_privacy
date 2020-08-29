from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import os

print('File to decrypt: ', end=' ')
file_name = input()

if not os.path.exists(file_name):
    print('File Does not exist')
    exit()

data = None
with open(file_name, 'rb') as fs:
    data = fs.read()

print('Enter Key: ', end=' ')
key = input().encode()

def decrypt(key, data):
    key = pad(key, 16)[:16]
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    original = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return original
name = file_name.split('.')[0]
with open(name + '.original', 'wb') as fs:
    fs.write(decrypt(key, data))