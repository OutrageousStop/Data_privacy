import pickle
import os

print('Enter useraname: ', end=' ')
user = input()
print('File: ', end=' ')
file_name = input()
print('Enter key: ', end=' ')
key = input()

if not os.path.exists('users.store.db'):
    users_list = {}
    with open('users.store.db', 'wb') as fs: 
        pickle.dump(users_list, fs)

users_list = None
with open('users.store.db', 'rb') as fs:
    users_list = pickle.load(fs)
if user not in users_list:
    users_list[user] = {}
users_list[user][file_name] = key

with open('users.store.db', 'wb') as fs:
    pickle.dump(users_list, fs)

print('Done')