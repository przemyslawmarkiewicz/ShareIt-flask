from flask import Flask
import os
from neo4j import GraphDatabase
from config import database_password, database_user, database_uri, secret_key


app = Flask(__name__)
app.secret_key = secret_key

driver = GraphDatabase.driver(uri=database_uri, auth=(database_user, database_password))
session = driver.session()

from app import views