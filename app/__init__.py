from flask import Flask
import os
from neo4j import GraphDatabase

app = Flask(__name__)

from app import views