import secrets
from flask import Blueprint, jsonify, make_response, request
from dbhelpers import run_statement, serialize_data;

from constants.columns import patient_columns, doctor_token_columns,token_columns, patient_signup_columns, doctor_columns, doctors_columns, doctor_signup_columns
from middleware.auth import validate_token


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
  # print(request.args.get("client_id"))
  try:

    doctor_id = request.args.get("doctor_id")

    result = run_statement('CALL get_doctor_by_id(?)', [doctor_id])

    doctor=serialize_data(doctor_columns, result)[0]

    # print("Fried", client_id)

    return make_response(jsonify(doctor),  200)
  except:
    return make_response("This is an error", 400)
 

# @doctor_bp.delete("/doctor-login")
# @validate_token
# def restaurant_logout():
#  try:
#   token = request.headers.get('token')
#   # print("CHECK THIS", token)
  
#   session_columns = ['restaurant_id', 'restaurant_token']
  
#   result = run_statement('CALL get_restaurant_session_by_token(?)', [token])
  
#   session = serialize_data(session_columns, result)[0]
  
#   # print("Pikin", session)

#   result = run_statement('CALL delete_restaurant_session(?)', [session['restaurant_id']])

#   # print("Omobaba", session['restaurant_id'])

#   return make_response(jsonify("You have successfully logged Out"),  200)
#  except:
#   return make_response("This is an error", 400)
 
# @doctor_bp.get("/secured")
# @validate_token
# def secured_route():
#   print("this is a test")
#   try:
#     return make_response(jsonify("This is a private route"),  200)
#   except:
#     return make_response("This is an error", 400)

# @doctor_bp.post("/doctor")
# def doctor_signup():
#  try:
#   name = request.json.get('name') 
#   email_address = request.json.get('email_address') 
#   address = request.json.get('address') 
#   phone_number = request.json.get('phone_number') 
#   bio = request.json.get('bio') 
#   city = request.json.get('city') 
#   profile_url = request.json.get('profile_url')
#   banner_url = request.json.get('banner_url') 
#   password = request.json.get('password') 
  
#   result = run_statement('CALL restaurant_signup(?,?,?,?,?,?,?,?,?)', [name, email_address, address, phone_number, bio, city, profile_url, banner_url, password])
  
#   # print(result)

#   restaurant = serialize_data(doctor_signup_columns, result)[0]

#   # print(client)

#   return make_response(jsonify(restaurant),  200)
#  except:
#   return make_response("This is an error", 400)

# @doctor_bp.patch("/restaurant")
# @validate_token
# def restaurant_update():
#  try:

#   # Creating a empty obj to hold either passed value or None for later updating
#   restaurant_data = {}

#   # TO DO

#   restaurant_data['name'] = request.json.get('name') if request.json.get('name') else None
#   restaurant_data['email_address'] = request.json.get('email_address') if request.json.get('email_address') else None
#   restaurant_data['address'] = request.json.get('address') if request.json.get('address') else None
#   restaurant_data['phone_number'] = request.json.get('phone_number') if request.json.get('phone_number') else None
#   restaurant_data['bio'] = request.json.get('bio') if request.json.get('bio') else None
#   restaurant_data['city'] = request.json.get('city') if request.json.get('city') else None
#   restaurant_data['profile_url'] = request.json.get('profile_url') if request.json.get('profile_url') else None
#   restaurant_data['banner_url'] = request.json.get('banner_url') if request.json.get('banner_url') else None
#   restaurant_data['password'] = request.json.get('password') if request.json.get('password') else None
  

#   # print(patient_data)

#   token = request.headers.get('token')
#   # print("CHECK THIS", token)
  
#   session_columns = ['restaurant_id', 'restaurant_token']

#   result = run_statement('CALL get_restaurant_session_by_token(?)', [token])
  
#   session = serialize_data(session_columns, result)[0]

#   # print(session)
  
#   result = run_statement(
#    'CALL update_restaurant(?,?,?,?,?,?,?,?,?,?)', 
#    [
#     session['restaurant_id'],
#     restaurant_data['name'],
#     restaurant_data['email_address'],
#     restaurant_data['address'],
#     restaurant_data['phone_number'],
#     restaurant_data['bio'],
#     restaurant_data['city'],
#     restaurant_data['profile_url'],
#     restaurant_data['banner_url'],
#     restaurant_data['password']
#   ]
#   )
  
#   print(result)
#   # client = serialize_data(client_columns, result)[0]

#   return make_response(jsonify("Restaurant succesfully updated"),  200)
#  except:
#   return make_response("This is an error", 400)
 
# @doctor_bp.delete("/doctor")
# @validate_token
# def delete_resturant():
#  try:
  
#   password_input = request.json.get('password')
#   token = request.headers.get('token')
#   # print("CHECK THIS", token)
  
#   result = run_statement('CALL get_restaurant_session_by_token(?)', [token])

#   session = result[0]
#   id = session[0]

#   result = run_statement('CALL get_restaurant_by_id(?)',[id])
  
#   restaurant=result[0]
#   # print(restaurant)
#   password = restaurant[9]
#   # print(password)
#   id = restaurant[0]
#   # print(id)

#   if (password != password_input):
#     return make_response(jsonify("Wrong Password"), 403)
  
#   result = run_statement('CALL delete_restaurant(?)', [id])

#   return make_response(jsonify("Restaurant Deleted"),  200)
#  except:
#   return make_response("This is an error", 400)
 
