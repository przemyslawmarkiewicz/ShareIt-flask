from flask import Flask
import os
from neo4j import GraphDatabase
from config import database_password, database_user, database_uri, secret_key


app = Flask(__name__)
app.secret_key = secret_key

from app import views