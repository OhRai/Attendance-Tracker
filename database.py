import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://attendance-tracker-b37e9-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    '123456':
    {
        'name': 'Elon Musk',
        'major': 'Engineering',
        'starting_year': 2020,
        'total_attendance': 6,
        'standing': 'G',
        'year': 2,
        'last_attended': '2023-5-15 17:53:50'
    },

    '231523':
    {
        'name': 'Barack Obama',
        'major': 'Politics',
        'starting_year': 2019,
        'total_attendance': 10,
        'standing': 'G',
        'year': 4,
        'last_attended': '2023-5-15 16:50:50'
    },

    '727727':
    {
        'name': 'Raiyan Samin',
        'major': 'Computer Engineering',
        'starting_year': 2022,
        'total_attendance': 10,
        'standing': 'G',
        'year': 1,
        'last_attended': '2023-5-15 18:53:50'
    }
}

for key, value in data.items():
    ref.child(key).set(value)