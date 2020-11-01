from flask import Flask, redirect, render_template, request, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import app.config as config
import app.utils as utils
import app.photoshop as photoshop

app = Flask(__name__)
config.configure_app(app)
db = SQLAlchemy(app)

class Template(db.Model):
    __tablename__ = "templates"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable = False, unique = True)
    image_url = db.Column(db.String(2048), nullable = False)
    created = db.Column(db.DateTime(), default = db.func.now())
    text_nodes = db.relationship("TextNode", backref = "template")

class TextNode(db.Model):
    __tablename__ = "text_nodes"
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(64), nullable = False, server_default = "")
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    r = db.Column(db.Integer)
    g = db.Column(db.Integer)
    b = db.Column(db.Integer)
    index = db.Column(db.Integer)
    template_id = db.Column(db.Integer(), db.ForeignKey('templates.id', ondelete = 'CASCADE'))
    
    def get_coordinates_string(self):
        return "({}, {})".format(self.x, self.y)
    def get_rgb_string(self):
        return "({}, {}, {})".format(self.r, self.g, self.b)

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

@app.route("/forms/create-template/", methods = ["POST"])
def create_template_form():
    img_url = request.form["img_url"]
    template_name = request.form["template_name"]
    if not utils.is_valid_template_name(template_name):
        return "Invalid template name!"
    template = Template(image_url = img_url, name = template_name)
    db.session.add(template)
    db.session.commit()
    return redirect("/")

@app.route("/manual/")
def manual_write_on_image():
    reqd_template = request.args.get("t", None)
    if not reqd_template:
        return "Need a template!"
    image_option = utils.manual_get_image_option(reqd_template)
    if image_option == 0:
        image_url = reqd_template
    else:
        if image_option == 1:
            template = Template.query.get(reqd_template)
        else:
            template = Template.query.filter(Template.name == reqd_template).first()
        if not template:
            return "Template not found!"
        image_url = template.image_url
    coords_dict = utils.unpack_coordinate_parameters(request.args)
    img_bytesio = photoshop.write_on_image_with_coords_dict(image_url, coords_dict)
    return send_file(img_bytesio, mimetype = 'image/jpeg')

@app.route("/templates/<template_name>/")
def specific_template_page(template_name):
    template = Template.query.filter(Template.name == template_name).first()
    if not template:
        return "Template with that name not found!"
    text_nodes = template.text_nodes
    text_nodes.sort(key = lambda x : x.index)
    return render_template("template.html", template = template, text_nodes = text_nodes)