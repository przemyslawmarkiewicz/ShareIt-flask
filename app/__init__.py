from flask import Flask
import os
from neo4j import GraphDatabase


app = Flask(__name__)
app.secret_key = os.urandom(24)

driver = GraphDatabase.driver(uri="bolt://149.156.109.37:7687", auth=("u7markiewicz", "291630"))
session = driver.session()

from app import views