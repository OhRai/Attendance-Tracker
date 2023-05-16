import cv2
import os
import pickle
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://attendance-tracker-b37e9-default-rtdb.firebaseio.com/',
    'storageBucket':'attendance-tracker-b37e9.appspot.com'
})

# Imports the student images
folder_path = 'Students'
path_list = os.listdir(folder_path)
print(path_list)
img_list = []
student_ids = []

for path in path_list:
    img_list.append(cv2.imread(os.path.join(folder_path, path))) # Images
    student_ids.append(os.path.splitext(path)[0])   # Student IDs

    file_name = f'{folder_path}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)


print(student_ids)

# Encoding
def find_encodings(image_list):
    encode_list = []
    for img in image_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)

    return encode_list

print('Encoding Started...')
encode_list_known = find_encodings(img_list)
encode_list_known_ids = [encode_list_known, student_ids]
print(encode_list_known)
print('Encoding Complete')

file = open('encode_file.p', 'wb')
pickle.dump(encode_list_known_ids, file)
file.close()
print('File Saved')
