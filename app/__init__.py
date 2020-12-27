from flask import Flask
import os
from neo4j import GraphDatabase
# from config import database_password, database_user, database_uri, secret_key


app = Flask(__name__)

from app import views