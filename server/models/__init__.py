from flask_sqlalchemy import SQLAlchemy
from firebase_admin import credentials, firestore, initialize_app

db = SQLAlchemy()

#Initialize Cloud Firestore
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db_events = firestore.client()
todo_ref = db_events.collection('todos')