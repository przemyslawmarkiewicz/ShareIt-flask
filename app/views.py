from flask import render_template, session
from app import app
from flask import Flask, render_template


@app.route('/')
def index():
    return render_template("_base.html")
    

    