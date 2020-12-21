from flask import render_template, session
from app import app
from flask import Flask, render_template
import os

@app.route('/')
def index():
    print(os.environ.get("DATABASE_USER"))
    return render_template("_base.html")
    

    