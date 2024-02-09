import secrets
from flask import Blueprint, jsonify, make_response, request
from dbhelpers import run_statement, serialize_data;

from constants.columns import patient_columns, doctor_token_columns,token_columns, patient_signup_columns, doctor_columns, doctors_columns, doctor_signup_columns
from middleware.auth import validate_token, validate_doctor_token


doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.post("/doctor-login")
def doctor_login():
 try:
  email_address = request.json.get('email_address')
  password = request.json.get('password')

  # print(email_address, password)
  
  result = run_statement('CALL get_doctor_by_email(?)', [email_address])

  # print("what is this", result)

  if (len(result)<1):
   return make_response(jsonify("Email not in use"), 401)
  
  doctor = serialize_data(doctor_columns, result)[0]

  if (doctor["password"] != password):
   return make_response(jsonify("Wrong Password"), 403)
  
  result = run_statement('CALL delete_doctor_session(?)', [doctor["id"]])

  token_string = secrets.token_hex(16)
  
  result = run_statement('CALL post_doctor_login(?,?)', [doctor["id"], token_string])

  token = serialize_data(doctor_token_columns, result)[0]

  return make_response(jsonify(token),  200)
 except:
  return make_response("This is an error", 400)
 
@doctor_bp.get("/doctors")
# @validate_restaurant_token

def get_all_doctor():
  
  try:

    result = run_statement('CALL get_all_doctors')

    all_doctors = serialize_data(doctors_columns, result)

    return make_response(jsonify(all_doctors),  200)
  except:
    return make_response("This is an error", 400)
  

# @doctor_bp.get("/doctor/<id>")
# @validate_token
# def get_doctor(id):
  
#   try:
#     result = run_statement('CALL get_doctor_by_id(?)', [id])

#     doctor = serialize_data(doctors_columns, result)[0]

#     return make_response(jsonify(doctor),  200)
#   except:
#     return make_response("This is an error", 400)
  
@doctor_bp.get("/doctor")
# @validate_token
# add validate_token if you want the user to sign in first before viewing another user
def get_doctor():
 
  try:

    doctor_id = request.args.get("doctor_id")

    result = run_statement('CALL get_doctor_by_id(?)', [doctor_id])

    doctor=serialize_data(doctor_columns, result)[0]

    # print("Fried", client_id)

    return make_response(jsonify(doctor),  200)
  except:
    return make_response("This is an error", 400)
 

@doctor_bp.delete("/doctor-login")
@validate_doctor_token
def doctor_logout():
 try:
  token = request.headers.get('token')
  # print("CHECK THIS", token)
  
  session_columns = ['doctor_id', 'token']
  
  result = run_statement('CALL get_doctor_session_by_token(?)', [token])
  
  session = serialize_data(session_columns, result)[0]
  
  # print("Pikin", session)

  result = run_statement('CALL delete_doctor_session(?)', [session['doctor_id']])

  return make_response(jsonify("You have successfully logged Out"),  200)
 except:
  return make_response("This is an error", 400)
 

@doctor_bp.post("/doctor")
def doctor_signup():
 try:
  first_name = request.json.get('first_name') 
  last_name = request.json.get('last_name') 
  medical_id = request.json.get('medical_id') 
  speciality = request.json.get('speciality') 
  email_address = request.json.get('email_address') 
  password = request.json.get('password') 
  image_url = request.json.get('image_url')
  
  result = run_statement('CALL add_new_doctor(?,?,?,?,?,?,?)', [first_name, last_name, medical_id, speciality, email_address, password, image_url])
  
  # print(result)

  doctor = serialize_data(doctor_signup_columns, result)[0]

  # print(client)

  return make_response(jsonify(doctor),  200)
 except:
  return make_response("This is an error", 400)

@doctor_bp.patch("/doctor")
@validate_doctor_token
def doctor_update():
 try:

  # Creating a empty obj to hold either passed value or None for later updating
  doctor_data = {}

  # TO DO

  doctor_data['first_name'] = request.json.get('first_name') if request.json.get('first_name') else None
  doctor_data['last_name'] = request.json.get('last_name') if request.json.get('last_name') else None
  doctor_data['medical_id'] = request.json.get('medical_id') if request.json.get('medical_id') else None
  doctor_data['speciality'] = request.json.get('speciality') if request.json.get('speciality') else None
  doctor_data['email_address'] = request.json.get('email_address') if request.json.get('email_address') else None
  doctor_data['password'] = request.json.get('password') if request.json.get('password') else None
  doctor_data['image_url'] = request.json.get('image_url') if request.json.get('image_url') else None


  token = request.headers.get('token')
 
  
  session_columns = ['doctor_id', 'token']

  result = run_statement('CALL get_doctor_session_by_token(?)', [token])
  
  session = serialize_data(session_columns, result)[0]

  # print(session)
  
  result = run_statement(
   'CALL update_doctor(?,?,?,?,?,?,?,?)', 
   [
    session['doctor_id'],
    doctor_data['first_name'],
    doctor_data['last_name'],
    doctor_data['medical_id'],
    doctor_data['speciality'],
    doctor_data['email_address'],
    doctor_data['password'],
    doctor_data['image_url']

    ]
  )
  
  # print(result)
  # client = serialize_data(client_columns, result)[0]

  return make_response(jsonify("Your profile is succesfully updated"),  200)
 except:
  return make_response("This is an error", 400)
 
@doctor_bp.delete("/doctor")
@validate_doctor_token
def delete_doctor():
 try:
  
  password_input = request.json.get('password')
  token = request.headers.get('token')
  # print("CHECK THIS", token)
  
  result = run_statement('CALL get_doctor_session_by_token(?)', [token])

  session = result[0]
  id = session[0]

  result = run_statement('CALL get_doctor_by_id(?)',[id])
  
  doctor=result[0]
  # print(restaurant)
  password = doctor[6]
  # print(password)
  id = doctor[0]
  # print(id)

  if (password != password_input):
    return make_response(jsonify("Wrong Password"), 403)
  
  result = run_statement('CALL delete_doctor(?)', [id])

  return make_response(jsonify("Doctor Deleted"),  200)
 except:
  return make_response("This is an error", 400)
 
