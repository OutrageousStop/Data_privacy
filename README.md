## Install the following
pip3 install pycryptodome
pip3 install opencv-python
pip3 install face_recognition           ** works on Linux

## To use the application
cmd -> python3 face_recog.py "file name"

Use encrypt.py to encrypt any data.
Use make_key to assign keys to users to access the files.

# Example: 
User - Ronaldo 
File access - dummy.data

## 1. Admin will encrypt the data
cmd -> python3 encrypt.py
    -> dummy.data
    -> abc                          ** This is the key which will be required for the users to decrypt the data.
done.
A new file will be generated -> dummy.data.encrypted

## 2. Admin will give access to specific users (for this example - Ronaldo)
cmd -> python3 make_key.py
    -> Ronaldo
    -> dummy.data.encrypted
    -> abc

## 3. Start the application 
cmd -> python3 face_recog.py dummy.data.encrypted
Then show any latest image of Ronaldo 

A new file will be generated -> dummy.data.original

### 1 - 3 can be reduced to a single command (for review 3)
### CSV anonymizer will be added to the project (for review 3)


