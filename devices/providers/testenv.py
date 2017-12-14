from dotenv import load_dotenv, find_dotenv
from os import environ

load_dotenv(find_dotenv())


print(environ.get("FIREBASE_API_KEY"))