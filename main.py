from flask import Flask, render_template,request,flash
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename
import os
import cv2
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = { 'webp' 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FOLDER']='uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def processImage(filename,operation):
    print(f"filename is {filename} and operation is {operation}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "2":
            imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newname=f"static/{filename}"
            cv2.imwrite(newname,imgProcessed)
            return newname

        case "1":
            newname=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newname,img)
            return newname
        case "3":
            newname=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newname,img)
            return newname
        case "4":
            newname=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newname,img)
            return newname








    pass

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/edit',methods=["POST","GET"])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return 'error'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'ERROR No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation)
            flash(f"Your image has been converted and available <a href='/{new}' target='_blank'>here</a>")
            return render_template('index.html')
    
    
    return render_template('index.html')
app.run(debug=True)