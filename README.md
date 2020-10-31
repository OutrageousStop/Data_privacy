## Install the following
pip3 install pycryptodome <br />
pip3 install opencv-python <br />
pip3 install face_recognition           ** works on Linux

## To use the application
cmd -> python3 face_recog.py "file name" <br />

Use encrypt.py to encrypt any data. <br />
Use make_key to assign keys to users to access the files. 

# Example: 
User - Ronaldo <br />
File access - dummy.data

## 1. Admin will encrypt the data
cmd -> python3 encrypt.py <br />
    -> dummy.data <br />
    -> abc                          ** This is the key which will be required for the users to decrypt the data. <br />
done. <br />
A new file will be generated -> dummy.data.encrypted

## 2. Admin will give access to specific users (for this example - Ronaldo)
cmd -> python3 make_key.py <br />
    -> Ronaldo <br />
    -> dummy.data.encrypted <br />
    -> abc

## 3. Start the application 
cmd -> python3 face_recog.py dummy.data.encrypted <br />
Then show any latest image of Ronaldo <br />

A new file will be generated -> dummy.data.original <br />

### 1 - 3 can be reduced to a single command (for review 3)
### CSV anonymizer will be added to the project (for review 3)


# Review 3 Changes done
