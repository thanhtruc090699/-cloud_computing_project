from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection setup
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(mongo_uri)
db = client["public_notes"]

# Import routes
from app import routes

