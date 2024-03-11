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
	
	return render_template('patient.jinja2', patient=patient.serialize())

@app.route('/patient/<ID>', methods=['PUT'])
def update_patient(ID):
	print(ID)
	data = request.form
	print(data)
	if not data: return jsonify({"error": "No data received."}), 400

	patient = database.Patient.query.get(ID)
	if not patient:
		return jsonify({'error': 'Patient not found'}), 404
	
	if data['fname']: patient.fname = data['fname']
	if data['lname']: patient.lname = data['lname']
	patient.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
	patient.gender = data['gender']
	patient.condition = data['condition']
	patient.treatment = data['treatment']
	
	try:
		database.db.session.commit()
		return jsonify({'message': 'Patient data updated successfully'})
	except Exception as e:
		return jsonify({'error': str(e)}), 500
	
@app.route('/search', methods=['GET'])
def search():
	return send_from_directory('static', 'search.html')

@app.route('/search_by_id', methods=['GET'])
def search_by_id():
	data = request.args.get('id')
	if not data: return jsonify({"error": "No data received."}), 400
	
	patient = database.Patient.query.get(data)
	
	if not patient:
		return jsonify({'error': 'Patient not found'}), 404
	else: return jsonify([patient.serialize()]), 200
	
@app.route('/search_by_condition', methods=['GET'])
def search_by_condition():
	data = request.args.get('condition')
	if not data: return jsonify({"error": "No data received."}), 400
	
	patients = database.Patient.query.filter_by(condition=data).all()
	
	if not patients:
		return jsonify({'error': 'Patient not found'}), 404
	else: return jsonify([patient.serialize() for patient in patients]), 200