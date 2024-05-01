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
    
    uploads = get_db().query(Upload).all()
    return render_template('view.html', collections=uploads)

@app.route('/predict/<int:id>', methods=['GET', 'POST'])
def predict(id):
    
    upload = get_by_id(Upload, id)
    score1 = 0
    score2 = 0
    resp = None
    if request.method == 'POST':
        try:
            resp = query(upload.image)
            if len(resp) == 0:
                flash('Predict failed', 'danger')
                return redirect('/view')
            label1 = resp[0]['label']
            score1 = resp[0]['score']
            label2 = resp[1]['label']
            score2 = resp[1]['score']
            if score1 > score2:
                ans = True
                score = round(score1 * 100,3)
            else:
                ans = False  
                score = round(score2 * 100,2)
            result = Result(
                image = upload.image,
                result = ans,
                score = score
            )
            save_to_db(result)
            flash('Predict success', 'success')
        except Exception as e:
            print(e)
            flash('Predict failed', 'danger')
    return render_template('predict.html', upload=upload, result=resp, score1=round(score1 * 100,2), score2=round(score2 * 100,2))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    db = get_db()
    upload = db.query(Upload).filter_by(id=id).first()
    db.delete(upload)
    db.commit()
    if os.path.exists(upload.image):
        os.remove(upload.image)
    db.close()
    return redirect('/view')

@app.route('/delete/pred/<int:id>', methods=['GET', 'POST'])
def delete_pred(id):
    db = get_db()
    result = db.query(Result).filter_by(id=id).first()
    db.delete(result)
    db.commit()
    if os.path.exists(result.image):
        os.remove(result.image)
    db.close()
    return redirect('/history')

@app.route('/history', methods=['GET', 'POST'])
def history():
    results = get_db().query(Result).all()
    return render_template('history.html', collections=results)


@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('report.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 