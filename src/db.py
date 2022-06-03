import os
from flask import Flask 
from flask_cors import CORS 
from flask_pymongo import PyMongo 
from dotenv import load_dotenv

load_dotenv()
MONGO_PWD = os.getenv('MONGO_PWD')

app = Flask(__name__, instance_relative_config=True)
app.config["MONGO_URI"] = f"mongodb+srv://Awwal123:{MONGO_PWD}@cluster0.k1tbsgh.mongodb.net/test"
mongo = PyMongo(app)

CORS(app)

db1 = mongo.db.templates
db2 = mongo.db.users
