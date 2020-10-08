import face_recognition
import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import pickle
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad


mypath = "./Photos"
if len(sys.argv) <= 1:
    print("Give File Name!!")
    exit()
file_name = sys.argv[1]

data = None
if not os.path.exists(file_name):
    print('File Does not exist')
    exit()

data = None
with open(file_name, 'rb') as fs:
    data = fs.read()

iv = data[:16]
ciphertext = data[16:]

users_list = None
with open('users.store.db', 'rb') as fs:
    users_list = pickle.load(fs)

video_capture = cv2.VideoCapture(0)
users = [f for f in listdir(mypath) if isfile(join(mypath, f))]

users_images = {name[:-4]: face_recognition.load_image_file(mypath + "/" + name) for name in users}
users_face_encodings = {name[:-4]: face_recognition.face_encodings(users_images[name[:-4]])[0] for name in users}
users = [i[:-4] for i in users]

known_face_encodings = [users_face_encodings[name] for name in users]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = users[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
    flag = 0
    for name in face_names:
        print(name)
        if name in users_list:
            flag = 1
            print('here')
            if file_name not in users_list[name]:
                break
            key = pad(users_list[name][file_name].encode(), 16)[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv = iv)
            original = unpad(cipher.decrypt(ciphertext), AES.block_size)
            new_name = file_name.split('.')[0]
            with open(new_name + '.original', 'wb') as fs:
                fs.write(original)
                print('Success')
                video_capture.release()
                cv2.destroyAllWindows()
                exit()

    if flag == 1:
        print(users_list)
        print(file_name)
        print("User Not Authorized")
        video_capture.release()
        cv2.destroyAllWindows()
        exit()
    
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()