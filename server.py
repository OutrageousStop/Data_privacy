from flask import Flask, flash, request, redirect, url_for, send_file, render_template, Response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import camera
from vcsave import VideoCameraSave
import pickle

app = Flask(__name__)

got_names = []

def gen(camera):
    while True:
        frame, names = camera.get_frame()
        global got_names
        got_names = names
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/access')
def access():
    return 'hello'

@app.route('/anonymize')
def anonymize_Encrypt():
    return render_template('Anonymize_and_Encrypt.html')

@app.route('/anonymize/upload_file', methods=["POST"])
def process_file():
    f = request.files['upload_file']
    key = request.form['Enc_key'].encode()
    f.save('./working_data/workingfile')
    with open('./working_data/workingfile', 'rb') as f:
        data = f.read()
    def encrypt(data, cipher):
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return ciphertext
        
    with open('./working_data/workingfile' + '.encrypted', 'wb') as fs:
        key = pad(key, 16)[:16]
        cipher = AES.new(key, AES.MODE_CBC)
        fs.write(cipher.iv)
        fs.write(encrypt(data, cipher))
    
    return send_file('./working_data/workingfile.encrypted')

@app.route('/grant_permission')
def grant_permission():
    return render_template('Grant_permission.html')

@app.route('/grant_permission/process', methods=["POST"])
def grant_permission_process():
    user = request.form["username"]
    key = request.form["Enc_key"]
    file_name = request.form["filename"]
    if not os.path.exists('users.store.db'):
        users_list = {}
        with open('users.store.db', 'wb') as fs: 
            pickle.dump(users_list, fs)
    with open('users.store.db', 'rb') as fs:
        users_list = pickle.load(fs)
    if user not in users_list:
        users_list[user] = {}
    users_list[user][file_name] = key
    with open('users.store.db', 'wb') as fs:
        pickle.dump(users_list, fs)
    return "Done"

@app.route('/video_stream')
def videostream():
    return Response(gen(camera.VideoCamera()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

def newEntry(camera, name):
    while True:
        frame = camera.newMember(name)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/api/addface/<name>')
def addface_API(name):
    return Response(newEntry(VideoCameraSave(), name),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/addface')
def addface():
    return render_template('addface.html')

@app.route('/addface_face_part', methods=["POST"])
def addface_face_part():
    username = request.form["username"]
    return render_template('addface_face_part.html', name=username)

@app.route('/addface_success')
def addface_success():
    return render_template('addface_success.html')

@app.route('/access_file')
def access_file():
    return render_template('access_file.html')

@app.route('/validate_access', methods = ["POST"])
def validate():
    f = request.files["upload_file"]
    file_name = request.form["filename"]
    key = request.form["Enc_key"]
    f.save('./working_data/current')
    with open('./working_data/current', 'rb') as fs:
        data = fs.read()
    
    iv = data[:16]
    ciphertext = data[16:]
    
    with open('users.store.db', 'rb') as fs:
        users_list = pickle.load(fs)
    
    global got_names
    flag = 0
    for name in got_names:
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
            return send_file(new_name + '.original')
    if flag == 1:
        return "Not allowed"
    
    return "none"


if __name__ == "__main__":
    app.run()