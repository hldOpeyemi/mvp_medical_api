from flask import Flask, request, jsonify, make_response
from dbhelpers import run_statement, serialize_data

def validate_token(func):
 def wrapper(*args, **kwargs):

  print("Running middle ware")

  patient_token = request.headers.get("token")
  if (patient_token == None or patient_token == ""):
   return make_response(jsonify("Please provide a token"), 403)
  
  result = run_statement('CALL validate_patient_token(?)', [patient_token])

  if (len(result) == 0):
   return make_response(jsonify("invalid token, please login"), 403)
  
  # print("Jollof Rice", result)

  response = func(*args, **kwargs)


  return response
  #Renaming the function name:
 wrapper.__name__ = func.__name__
 return wrapper


def validate_doctor_token(func):
 def doctor_wrapper(*args, **kwargs):

  # print("Running middle ware")

  doctor_token = request.headers.get("token")
  if (doctor_token == None or doctor_token == ""):
   return make_response(jsonify("Please provide a token"), 403)
  
  result = run_statement('CALL validate_doctor_token(?)', [doctor_token])

  if (len(result) == 0):
   return make_response(jsonify("invalid token, please login"), 403)
  
  # print("FriedRice", result)

  response = func(*args, **kwargs)


  return response
 doctor_wrapper.__name__ = func.__name__
 return doctor_wrapper