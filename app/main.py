from flask import Flask, redirect, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def home_page_view():
    return "hello :)"

@app.route("/write-on-image/")
def write_on_image_page():
    return render_template("write_on_image.html")

@app.route("/assets/<path:file_path>")
def get_asset_file(file_path):
    path = os.path.join(os.path.dirname(__file__), "assets")
    return send_from_directory(path, file_path, as_attachment = True)