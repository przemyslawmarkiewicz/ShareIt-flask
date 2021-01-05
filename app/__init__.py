from flask import Flask
from flask_session import Session
import os
from neo4j import GraphDatabase


app = Flask(__name__)

sess = Session()
sess.init_app(app)

from app import views