import pyrebase
import requests
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from os import environ
load_dotenv(find_dotenv())
config = {
  "apiKey": environ.get("FIREBASE_API_KEY"),
  "authDomain": environ.get("FIREBASE_PROJECT_NAME")+".firebaseapp.com",
  "databaseURL": environ.get("FIREBASE_PROJECT_NAME")+".firebaseio.com",
  "storageBucket": environ.get("FIREBASE_PROJECT_NAME")+".appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
# auth = firebase.auth()
# user = auth.sign_in_with_email_and_password('username', 'password')

def logData(temp,humid,light):
  data = {"temp": temp,"humid":humid,"light":light}
  # db.child("room").child(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).set(data,user['idToken'])
  db.child("room").child(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).set(data)

def getPlugStatus():  
  # data = dict(db.child("devices").get().val())
  
  data = requests.get('https://'+environ.get("FIREBASE_PROJECT_NAME")+'.firebaseio.com/devices.json',timeout=20).json()
  # print(data)
  return data['outlet1']['status'],data['outlet2']['status']

def getPlugData():  
  data = requests.get('https://'+environ.get("FIREBASE_PROJECT_NAME")+'.firebaseio.com/devices.json',timeout=20).json()  
  return data['outlet1'],data['outlet2']

def updateData(temp,humid,light,power):
   data = requests.post('https://'+environ.get("FIREBASE_PROJECT_NAME")+'.firebaseio.com/devices.json',timeout=20).json()

def updatePlugStatus(number,status):  
  db.child("devices/outlet"+str(number)).update({"status": status})

def getData():
  data = requests.get('https://'+environ.get("FIREBASE_PROJECT_NAME")+'.firebaseio.com/data.json',timeout=20).json()
  # print(data)
  return data['humid'],data['light'],data['temp'],data['time']