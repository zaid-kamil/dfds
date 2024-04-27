from database import User, Upload, Result, get_db, save_to_db, get_all, get_by_id
from flask import Flask, render_template, request, redirect, flash, session
from predictor import query
app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'


import os
from werkzeug.utils import secure_filename
# create folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
os.makedirs('static/models', exist_ok=True)

def save_session(user):
    session['id'] = user.id
    session['username'] = user.username
    session['email'] = user.email
    session['isauth'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_db().query(User).filter_by(username=username, password=password).first()
        if user:
            save_session(user)
            flash('Login success', 'success')
            return redirect('/upload')
        else:
            flash('Login failed', 'danger')
            url = request.url
            return redirect(url)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        files = request.files.getlist('files')
        for file in files:
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                upload = Upload(
                    image=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                    user = session['id']
                )
                save_to_db(upload)
                flash('Upload success', 'success')
        return redirect('/upload')
    return render_template('upload.html')


@app.route('/view', methods=['GET', 'POST'])
def view():
    if not session['isauth']:
        return redirect('/login')
    uploads = get_db().query(Upload).all()
    return render_template('view.html', collections=uploads)

@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('report.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 