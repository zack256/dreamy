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
    def set_coordinates_from_string(self, coordinate_string):
        self.x, self.y = utils.get_coordinates(coordinate_string)
    def set_rgb_from_string(self, rgb_string = "(0,0,0)"):
        self.r, self.g, self.b = utils.get_rgb(rgb_string)

@app.route("/")
def home_page_view():
    return render_template("index.html")

@app.route("/create-template/")
def write_on_image_page():
    return render_template("create_template.html")

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
    if not utils.is_valid_website(img_url):
        return "Invalid URL!"
    template = Template(image_url = img_url, name = template_name)
    db.session.add(template)
    db.session.commit()
    return redirect("/")

def get_image_url_helper(reqd_template):
    image_option = utils.manual_get_image_option(reqd_template)
    if image_option == 0:
        image_url = reqd_template
        template = None
    else:
        if image_option == 1:
            template = Template.query.get(reqd_template)
        else:
            template = Template.query.filter(Template.name == reqd_template).first()
        if not template:
            image_url = None
        else:
            image_url = template.image_url
    return image_url, template

@app.route("/manual/")
def manual_write_on_image():
    reqd_template = request.args.get("t", None)
    if not reqd_template:
        return "Need a template!"
    image_url, template = get_image_url_helper(reqd_template)
    if not image_url:
        return "Template not found!"
    coords_dict = utils.unpack_coordinate_parameters(request.args)
    img_bytesio = photoshop.write_on_image_with_coords_dict(image_url, coords_dict)
    return send_file(img_bytesio, mimetype = 'image/jpeg')

@app.route("/templates/")
def templates_page():
    templates = Template.query.order_by(Template.created).all()
    return render_template("templates.html", templates = templates)

@app.route("/templates/<template_name>/")
def specific_template_page(template_name):
    template = Template.query.filter(Template.name == template_name).first()
    if not template:
        return "Template with that name not found!"
    text_nodes = template.text_nodes
    text_nodes.sort(key = lambda x : x.index)
    return render_template("template.html", template = template, text_nodes = text_nodes)

@app.route("/t/")
def send_template_with_text_on_points():
    reqd_template = request.args.get("t", None)
    if not reqd_template:
        return "Need a template!"
    image_url, template = get_image_url_helper(reqd_template)
    if not image_url:
        return "Template not found!"
    if not template:
        return "This URL requires an image in the database!"
    text_nodes = template.text_nodes
    coords_dict = {}
    for text_node in text_nodes:
        reqd_label = request.args.get(str(text_node.index), None)
        if reqd_label:
            coords_dict[(text_node.x, text_node.y)] = reqd_label
    img_bytesio = photoshop.write_on_image_with_coords_dict(image_url, coords_dict)
    return send_file(img_bytesio, mimetype='image/jpeg')

@app.route("/forms/add-text-nodes/", methods = ["POST"])
def add_text_nodes_form():
    template = Template.query.get(request.form["templateid"])
    if not template:
        return "Template not found!"
    form_dict = {}
    for key, val in request.form.items():
        if "_" not in key:
            continue
        attr, num = key.split("_")
        if int(num) not in form_dict:
            form_dict[int(num)] = {}
        form_dict[int(num)][attr] = val
    tn_list = sorted(form_dict.keys())
    num_text_nodes = len(template.text_nodes)
    for tn_idx in tn_list:
        text_node = TextNode()
        text_node.set_coordinates_from_string(form_dict[tn_idx]["coords"])
        text_node.set_rgb_from_string()
        num_text_nodes += 1
        text_node.index = num_text_nodes
        text_node.template_id = template.id
        db.session.add(text_node)
    db.session.commit()
    return redirect("/templates/{}".format(template.name))