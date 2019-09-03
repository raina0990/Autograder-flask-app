from flask import Flask, render_template, request, flash
from werkzeug import secure_filename

import os
import subprocess

app = Flask(__name__)
app.secret_key = 'password'


# Home Page for Auto Grade System 

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # Upload the file
        if (f.filename == 'walk.cc'):
            f.save(secure_filename(f.filename))
            flash('File uploaded successfully!')
            # Compile and Execute the code
            subprocess.call("rm -f ./a.out", shell=True)
            retcode = subprocess.call("/usr/bin/g++ walk.cc", shell=True)
            if retcode:
                print("failed to compile walk.cc")
                exit
                flash("Failed to compile walk.cc!")
                flash ("Upload the file again!")
                return render_template('upload.html')

            subprocess.call("rm -f ./output", shell=True)
            retcode = subprocess.call("./test.sh", shell=True)
            message = "Score: " + str(retcode) + " out of 2 correct."
            message2 = " Compiled and executed successfully !"
            print (message)
            print("*************Original submission*************")
            with open('walk.cc','r') as fs:
                print(fs.read())
                flash(message2)
                flash(message)
            return render_template('result.html')
        elif (f.filename != 'walk.cc'):
            flash('Please upload walk.cc file only!')
            return render_template('upload.html')
        else :
            flash('No file chosen')
            return render_template('upload.html')

    

if __name__ ==  '__main__':
    app.run(host="0.0.0.0", debug=True)