from flask import Flask,session
app = Flask(__name__)
import os
app.secret_key = os.environ.get('SECRET_KEY')