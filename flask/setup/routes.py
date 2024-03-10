from flask import request, jsonify, send_from_directory, render_template
from datetime import datetime
from setup import app, database

@app.route('/', methods=['GET'])
def root():
	logged_in = request.cookies.get('loggedIn')
	if logged_in: return send_from_directory('static', 'dashboard.html')
	else: return send_from_directory('static', 'index.html')

@app.route('/patients/add', methods=['GET'])
def patient_add():
	return send_from_directory('static', 'add-patient.html')

@app.route('/patients', methods=['GET'])
def get_patients():
	patients = database.Patient.query.all()
	patients_data = [{'id': patient.id,	'fname': patient.fname,	'lname': patient.lname} for patient in patients]

	return render_template('patients.jinja2', patients=patients_data)

@app.route('/patients', methods=['POST'])
def add_patient():
	# Extract patient data from request
	patient_data = request.form
	print(patient_data)
	
    # Validate request body
	if not patient_data:
		return jsonify({"error": "No data received"}), 400
	
	# Create a new Patient instance
	patient = database.Patient(
		fname=patient_data['fname'],
		lname=patient_data['lname'],
		dob=datetime.strptime(patient_data['dob'], '%Y-%m-%d').date(),
	    gender=patient_data['gender'],
	    condition=patient_data['condition'],
	    treatment=patient_data['treatment']
	)
	
	# TODO: try and catch error on commit as the data may be formatted incorrectly.
    # Add the new patient to the database
	database.db.session.add(patient)
	database.db.session.commit()
	
	# Return success message
	return jsonify({"message": "Patient data received and stored successfully"}), 200

@app.route('/patient/<ID>', methods=['GET'])
def get_patient(ID):
	patient = database.Patient.query.get(ID)
	if not patient:
		return jsonify({'error': 'Patient not found'}), 404
	return jsonify(patient.serialize()), 200

@app.route('/patient/<ID>', methods=['PUT'])
def update_patient(ID):
	print(ID)
	patient = database.Patient.query.get(ID)
	if not patient:
		return jsonify({'error': 'Patient not found'}), 404
		
	data = request.json
	patient_data = {
		'fname': patient.fname,
		'lname': patient.lname,
		'dob': patient.dob,
		'gender': patient.gender,
		'condition': patient.condition,
		'treatment': patient.treatment
    }
	
	for field in ['fname', 'lname', 'dob', 'gender', 'condition', 'treatment']:
		if field in data:
			patient_data[field] = data[field]
	
	database.db.session.commit() # TODO: try and catch error on commit as the data may be formatted incorrectly.
	return jsonify({'message': 'Patient data updated successfully'})