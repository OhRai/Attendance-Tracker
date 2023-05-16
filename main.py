import cv2
import cvzone
import os
import numpy as np
import pickle
import face_recognition
from datetime import datetime

# Database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://attendance-tracker-b37e9-default-rtdb.firebaseio.com/',
    'storageBucket':'attendance-tracker-b37e9.appspot.com'
})

bucket = storage.bucket()

# Sets the dimensions of the webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

img_background = cv2.imread('Resources/Main Interface.png')

# Imports the different mode images into a list
folder_mode_path = 'Resources/Modes'
mode_path_list = os.listdir(folder_mode_path)
img_mode_list = []
for path in mode_path_list:
    img_mode_list.append(cv2.imread(os.path.join(folder_mode_path, path)))

# Load the encoding file
print('Loading Encode File...')
file = open('encode_file.p', 'rb')
encode_list_known_ids = pickle.load(file)
file.close()
encode_list_known, student_ids = encode_list_known_ids
print(student_ids)
print('Encode File Loaded')

mode_type = 0
counter = 0
id = -1
img_student = []

# Loading the Graphics and Webcam
while True:
    success, img = cap.read()

    img_small = cv2.resize(img, (0,0), None, 0.25, 0.25) # Rescale the webcam to 25% of the 640x480 size
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)  # Change the color from bgr to rgb

    face_cur_frame = face_recognition.face_locations(img_small)
    encode_cur_frame = face_recognition.face_encodings(img_small, face_cur_frame)

    img_background[180:180+480, 82:82+640] = img # Webcam
    img_background[42:42+636, 864:864+371] = img_mode_list[mode_type] #for the card on the right side

    if face_cur_frame:
        for encode_face, face_location in zip(encode_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face)
            face_distance = face_recognition.face_distance(encode_list_known, encode_face)

            match_idx = np.argmin(face_distance)

            if matches[match_idx]:

                # Create a box around the detected face
                y1, x2, y2, x1 = face_location 
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 
                bbox = 82+x1, 180+y1, x2-x1, y2-y1 
                img_background = cvzone.cornerRect(img_background, bbox, rt=0)

                id = student_ids[match_idx]

            if counter == 0:
                cvzone.putTextRect(img_background, 'Loading', (275, 400))
                cv2.imshow('Attendance Tracker', img_background)
                cv2.waitKey(1)
                counter = 1
                mode_type = 1
        
            if counter != 0:

                # Verifies student and updates the database
                if counter == 1:
                    student_info = db.reference(f'Students/{id}').get()

                    # Imports the student image from database
                    blob = bucket.get_blob(f'Students/{id}.jpg') # Gets the image
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    img_student = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    # Updates the data of attendance
                    date_time_object = datetime.strptime(student_info['last_attended'], '%Y-%m-%d %H:%M:%S')
                    seconds_elapsed = (datetime.now() - date_time_object).total_seconds()

                    if seconds_elapsed > 15:
                        # Total Attendance
                        ref = db.reference(f'Students/{id}')
                        student_info['total_attendance'] += 1
                        ref.child('total_attendance').set(student_info['total_attendance'])

                        # Last Attended
                        ref.child('last_attended').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                
                    else:
                        mode_type = 3
                        counter = 0

            if mode_type != 3:
                img_background[42:42+636, 864:864+371] = img_mode_list[mode_type]
            
                # Show the Marked Screen
                if 10 < counter < 20:
                    mode_type = 2
                
                img_background[42:42+636, 864:864+371] = img_mode_list[mode_type]

                # Show the Info Screen
                if counter <= 10:

                    cv2.putText(img_background, str(student_info['name']), (990, 472),
                                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
                    cv2.putText(img_background, str(id), (990, 536),
                                cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
                    
                    img_background[166:166+220, 940:940+220] = img_student

            counter += 1
        
            # Reset everything
            if counter >= 20:
                counter = 0
                mode_type = 0
                student_info = []
                img_student = []
                img_background[42:42+636, 864:864+371] = img_mode_list[mode_type] #for the card on the right side

    else: 
        mode_type = 0
        counter = 0

    cv2.imshow('Attendance Tracker', img_background)
    cv2.waitKey(1)

    # Exiting the program
    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit the loop when 'q' key is pressed
        break

cap.release()  # Release the webcam
cv2.destroyAllWindows()  # Destroy all windows