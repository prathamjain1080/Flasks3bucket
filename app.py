import boto3    
import uuid
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENTIONS = {'txt','pdf','png','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS


db = SQLAlchemy()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orignal_filename = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))


def create_app():
    app=Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///db.sqlite3"
    db.init_app(app)

    @app.route("/", methods =["GET","POST"])

    def index():
        if request.method == "POST":
            uploaded_file = request.files["file-to-save"]
            if not allowed_file(uploaded_file.filename):
                return "FILE NOT ALLOWED"
            

            new_filename=uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.',1)[1].lower()
            bucket_name="flasks3assign"
            s3 = boto3.resource('s3', region_name='ap-south-1')
            s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)


            return render_template("file_uploaded.html")
        
        files = File.query.all()
        return render_template("index.html", files=files)
    return app