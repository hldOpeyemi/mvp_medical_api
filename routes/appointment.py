import secrets
from flask import Blueprint, jsonify, make_response, request
import mariadb
from datetime import datetime, timedelta
import time

from dbhelpers import run_statement, serialize_data;

from constants.columns import appointment_columns
from middleware.auth import validate_token


appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.post("/appointment")
def add_new_appointment():
  try:
    
    patient_id = request.json.get('patient_id')
    doctor_id = request.json.get('doctor_id')
    appt_date = request.json.get('appt_date')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    status = request.json.get('status')
    # start_time_str = (datetime.min + start_time).strftime('%H:%M:%S')
    # end_time_str = (datetime.min + end_time).strftime('%H:%M:%S')
    # appt_date_str = appt_date.strftime('%Y-%m-%d')
  
    result = run_statement('CALL add_new_appointment(?,?,?,?,?,?)', [patient_id, doctor_id, appt_date, start_time, end_time, status])
    print("Changing", result)

    appointment = serialize_data(appointment_columns, result)[0]

    return make_response(jsonify(appointment),  200)
  except Exception as error:
    return make_response("ERROR", 400)

@appointment_bp.patch("/appointment")
def edit_appointment():
 try:

  # Creating a empty obj to hold either passed value or None for later updating
  appointment_data = {}
  appointment_data['patient_id'] = request.json.get('patient_id') if request.json.get('patient_id') else None
  appointment_data['doctor_id'] = request.json.get('doctor_id') if request.json.get('doctor_id') else None
  appointment_data['appt_date'] = request.json.get('appt_date') if request.json.get('appt_date') else None
  appointment_data['start_time'] = request.json.get('start_time') if request.json.get('start_time') else None
  appointment_data['end_time'] = request.json.get('end_time') if request.json.get('end_time') else None
  appointment_data['status'] = request.json.get('status') if request.json.get('status') else None

  result = run_statement('CALL edit_appointment(?,?,?,?,?,?,?,?,?,?,?)', 
   
   [
    appointment_data['id'],
    appointment_data['patient_id'],
    appointment_data['doctor_id'] ,
    appointment_data['appt_date'],
    appointment_data['start_time'],
    appointment_data['end_time'],
    appointment_data['status'],
    ])
  
  return make_response(jsonify("Appointment Succesfully Updated", result),  200)
 except:
  return make_response("This is an error", 400)
 

 
# @appointment_bp.delete("/appoitnment")

# def delete_appointment():
#  try:
  
#   password_input = request.json.get('password')
#   token = request.headers.get('token')
#   # print("CHECK THIS", token)
  
#   result = run_statement('CALL get_patient_session_by_token(?)', [token])

#   session = result[0]
#   id = session[0]

#   result = run_statement('CALL get_patient_by_id(?)',[id])
  
#   patient=result[0]
#   # print(restaurant)
#   password = patient[9]
#   # print(password)
#   id = patient[0]
#   # print(id)

#   if (password != password_input):
#     return make_response(jsonify("Wrong Password"), 403)
  
#   result = run_statement('CALL delete_patient(?)', [id])

#   return make_response(jsonify("Patient Deleted"),  200)
#  except:
#   return make_response("This is an error", 400)
 
# # @appointment_bp.get("/patient")
# # @validate_token
# # # add validate_token if you want the user to sign in first before viewing another user
# # def get_all_patients():
# #   # print(request.args.get("patient_id"))
# #   try:

# #     result = run_statement('CALL get_all_patients')

# #     return make_response(jsonify(result),  200)
# #   except:
# #     return make_response("This is an error", 400)
  

# @appointment_bp.delete("/patient-login")
# @validate_token
# def patient_logout():
#  try:
#   token = request.headers.get('token')
#   # print("CHECK THIS", token)
  
#   session_columns = ['patient_id', 'token']
  
#   result = run_statement('CALL get_patient_session_by_token(?)', [token])

#   session = serialize_data(session_columns, result)[0]
  
#   result = run_statement('CALL delete_patient_session(?)', [session['patient_id']])

#   return make_response(jsonify("You have successfully logged Out"),  200)
#  except:
#   return make_response("This is an error", 400)