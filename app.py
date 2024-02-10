from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from dbhelpers import run_statement, serialize_data
import json
import secrets
from middleware.auth import validate_token
from constants.columns import patient_columns, patient_token_columns, doctor_token_columns

# Routes Imports

from routes.patient import patient_bp
from routes.doctor import doctor_bp
from routes.appointment import appointment_bp

app = Flask(__name__)
CORS(app)

@app.get("/")
def health_check():
  return make_response("API online", 200)

@app.get("/private")
@validate_token
def private_router():
  print("this is a test")
  try:
    return make_response(jsonify("This is a private route"),  200)
  except:
    return make_response("This is an error", 400)
  


app.register_blueprint(patient_bp, url_prefix='/api')
app.register_blueprint(doctor_bp, url_prefix='/api')
app.register_blueprint(appointment_bp, url_prefix='/api')


app.run(debug=True)