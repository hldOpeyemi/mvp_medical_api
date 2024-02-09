import secrets
from flask import Blueprint, jsonify, make_response, request
import mariadb

from dbhelpers import run_statement, serialize_data;

from constants.columns import patient_columns, token_columns, patient_signup_columns, doctor_columns, doctors_columns, doctor_signup_columns
from middleware.auth import validate_token


patient_bp = Blueprint('patient', __name__)

@patient_bp.post("/patient-login")
def patient_login():
 try:
  email_address = request.json.get('email')
  password = request.json.get('password')
  
  result = run_statement('CALL patient_login(?,?)', [email_address, password])
  # print(len(result)) 

  if (len(result)<1):
   return make_response(jsonify("Email not in use"), 401)
  print(result)
  patient = serialize_data(patient_columns, result)[0]

  if (patient["password"] != password):
   return make_response(jsonify("Wrong Password"), 403)
  
  result = run_statement('CALL delete_patient_session(?)', [patient["id"]])

  token_string = secrets.token_hex(16)

  print(token_string)
  result = run_statement('CALL post_patient_login(?,?)', [patient["id"], token_string])

  token = serialize_data(token_columns, result)[0]

  return make_response(jsonify(token),  200)
 
 except:
  return make_response("This is an error", 400)

@patient_bp.get("/patient")
# @validate_token
# add validate_token if you want the user to sign in first before viewing another user
def get_patient():
 
  try:

    patient_id = request.args.get("patient_id")

    result = run_statement('CALL get_patient_by_id(?)', [patient_id])

    patient=serialize_data(patient_columns, result)[0]

    return make_response(jsonify(patient),  200)
  except:
    return make_response("This is an error", 400)
   
  # print("CHECK THIS", token)

@patient_bp.post("/patient")
def add_new_patient():
  try:
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    date_of_birth = request.json.get('date_of_birth')
    phone_number = request.json.get('phone_number')
    contact_address = request.json.get('contact_address') 
    health_card_number = request.json.get('health_card_number')
    email_address = request.json.get('email_address')
    password = request.json.get('password')
    gender = request.json.get('gender')
    emergency_contact =request.json.get('emergency_contact')

    # print(len([first_name, last_name, date_of_birth, phone_number, contact_address, health_card_number, email_address, password, gender, emergency_contact]), [first_name, last_name, date_of_birth, phone_number, contact_address, health_card_number, password, email_address, gender, emergency_contact])

    result = run_statement('CALL add_new_patient(?,?,?,?,?,?,?,?,?,?)', [first_name, last_name, date_of_birth, phone_number, contact_address, health_card_number, email_address, password, gender, emergency_contact])
    
    if (type(result) == mariadb.IntegrityError):
      return make_response(jsonify(str(result)), 400)

    patient = serialize_data(patient_signup_columns, result)[0]

    return make_response(jsonify(patient),  200)
  except Exception as error:
    return make_response("ERROR", 400)

@patient_bp.patch("/patient")
@validate_token
def patient_update():
 try:

  # Creating a empty obj to hold either passed value or None for later updating
  patient_data = {}

  # TO DO

  patient_data['first_name'] = request.json.get('first_name') if request.json.get('first_name') else None
  patient_data['last_name'] = request.json.get('last_name') if request.json.get('last_name') else None
  patient_data['date_of_birth'] = request.json.get('date_of_birth') if request.json.get('date_of_birth') else None
  patient_data['phone_number'] = request.json.get('phone_number') if request.json.get('phone_number') else None
  patient_data['contact_address'] = request.json.get('contact_address') if request.json.get('contact_address') else None
  patient_data['health_card_number'] = request.json.get('health_card_number') if request.json.get('health_card_number') else None
  patient_data['email_address'] = request.json.get('email_address') if request.json.get('email_address') else None
  patient_data['password'] = request.json.get('password') if request.json.get('password') else None
  patient_data['gender'] = request.json.get('gender') if request.json.get('gender') else None
  patient_data['emergency_contact'] = request.json.get('emergency_contact') if request.json.get('emergency_contact') else None
  

  print(patient_data)

  token = request.headers.get('token')
  # print("CHECK THIS", token)
  
  session_columns = ['patient_id', 'token']


  result = run_statement('CALL get_patient_session_by_token(?)', [token])
  
  session = serialize_data(session_columns, result)[0]

  print(session["patient_id"], type((session["patient_id"])))
  
  result = run_statement(
   'CALL update_patient(?,?,?,?,?,?,?,?,?,?,?)', 
   [
    session['patient_id'],
    patient_data['first_name'],
    patient_data['last_name'] ,
    patient_data['date_of_birth'],
    patient_data['phone_number'],
    patient_data['contact_address'],
    patient_data['health_card_number'],
    patient_data['email_address'],
    patient_data['password'],
    patient_data['gender'],
    patient_data['emergency_contact'] 
  ]
  )
  # ( v_id int, 
  #   v_first_name 
  # , v_last_name 
  # , v_date_of_birth 
  # , v_phone_number 
  # , v_contact_address 
  # , v_health_card_number 
  # , v_email_address 
  # , v_password 
  # , v_gender 
  # , v_emergency_contact 
  # )

  return make_response(jsonify("Patient Succesfully Updated"),  200)
 except:
  return make_response("This is an error", 400)
 
@patient_bp.delete("/patient")
@validate_token
def delete_patient():
 try:
  
  password_input = request.json.get('password')
  token = request.headers.get('token')
  # print("CHECK THIS", token)
  
  result = run_statement('CALL get_patient_session_by_token(?)', [token])

  session = result[0]
  id = session[0]

  result = run_statement('CALL get_patient_by_id(?)',[id])
  
  patient=result[0]
  # print(restaurant)
  password = patient[9]
  # print(password)
  id = patient[0]
  # print(id)

  if (password != password_input):
    return make_response(jsonify("Wrong Password"), 403)
  
  result = run_statement('CALL delete_patient(?)', [id])

  return make_response(jsonify("Patient Deleted"),  200)
 except:
  return make_response("This is an error", 400)
 
# @patient_bp.get("/patient")
# @validate_token
# # add validate_token if you want the user to sign in first before viewing another user
# def get_all_patients():
#   # print(request.args.get("patient_id"))
#   try:

#     result = run_statement('CALL get_all_patients')

#     return make_response(jsonify(result),  200)
#   except:
#     return make_response("This is an error", 400)
  

@patient_bp.delete("/patient-login")
@validate_token
def patient_logout():
 try:
  token = request.headers.get('token')
  # print("CHECK THIS", token)
  
  session_columns = ['patient_id', 'token']
  
  result = run_statement('CALL get_patient_session_by_token(?)', [token])

  session = serialize_data(session_columns, result)[0]
  
  result = run_statement('CALL delete_patient_session(?)', [session['patient_id']])

  return make_response(jsonify("You have successfully logged Out"),  200)
 except:
  return make_response("This is an error", 400)