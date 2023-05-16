# Attendance Tracker

The Attendance Tracker is a project that uses face recognition to track the attendance of students. It captures the faces of students using a webcam, compares them with known faces, and updates the attendance records in a Firebase database.

[Click Here to View Images of the Program](https://imgur.com/a/6gh7XfT)

## Features

- Real-time face detection and recognition
- Integration with Firebase for database management
- Attendance tracking based on student identification
- Visual interface with different modes (made with Figma)

## Requirements

You will need to install the Desktop Development with C++ on Visual Studio to install CMake
- OpenCV (4.5.3.56)
- cvzone (1.5.1)
- numpy (1.21.2)
- face-recognition (1.3.0)
- firebase-admin (5.1.0)
- CMake (3.21.3)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/attendance-tracker.git
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Obtain the necessary credentials:

   - Obtain the `serviceAccountKey.json` file for Firebase authentication.
   - Place the `serviceAccountKey.json` file in the project directory.

4. Set up the Firebase database:

   - Create a Firebase project and enable the Realtime Database.
   - Update the `'databaseURL'` and `'storageBucket'` values in the code with your Firebase project's details.

5. Prepare the resources:

   - Replace `'Resources/Main Interface.png'` with your desired interface image.
   - Place the mode images in the `'Resources/Modes'` folder.

## Usage

1. Run the script:

   ```bash
   python attendance_tracker.py
   ```

2. The webcam feed will open, and the program will start detecting and recognizing faces.

3. As recognized faces are matched with known faces, the attendance records will be updated in the Firebase database.

4. Press 'q' to quit the program.

## Acknowledgments

- [cvzone](https://github.com/cvzone/cvzone)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Firebase](https://firebase.google.com/)
