from flask_sqlalchemy import SQLAlchemy
import uuid

from setup import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
db = SQLAlchemy(app)

# Define the Patient model
class Patient(db.Model):
	id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
	fname = db.Column(db.String(64))
	lname = db.Column(db.String(64))
	dob = db.Column(db.Date)
	gender = db.Column(db.String(6)) # "Male", "Female" or "Other"
	condition = db.Column(db.String(2048)) # ~300 words
	treatment = db.Column(db.String(2048))

	def __repr__(self):
		return f'<Patient {self.id}>'
	
	def serialize(self):
		return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'dob': self.dob.isoformat(),
            'gender': self.gender,
            'condition': self.condition,
            'treatment': self.treatment
        }