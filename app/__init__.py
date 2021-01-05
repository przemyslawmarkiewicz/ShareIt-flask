from flask import Flask
from flask_session import Session
import os
from neo4j import GraphDatabase


app = Flask(__name__)

sess = Session()

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

sess.init_app(app)

from app import views