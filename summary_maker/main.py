import os
from flask.globals import request
from flask import Flask,session,flash,redirect,render_template,url_for
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from werkzeug.utils import secure_filename
from database import User, File, Profile
import re
from utils import *
from text_summarizer import text_summarizer
from audio_to_text import transcript


ALLOWED_EXTENSIONS = ['txt','pdf','wav','mp3', 'mp4', 'doc','docx', 'mov' , 'wmv', 'flv', 'avi' 'mkv', 'webm' ]
audio_type = ['wav','mp3']
video_type = ['mp4', 'mov' , 'wmv', 'flv', 'avi' 'mkv', 'webm' ]
document_type = ['txt','pdf','doc','docx']
app=Flask(__name__)
app.secret_key = "Srishti Trivedi"
app.config['UPLOAD_FOLDER'] = os.path.join('static','uploads')


def getdb():
    engine = create_engine('sqlite:///database.sqlite')
    Session = sessionmaker(bind=engine)
    return scoped_session(Session)

@app.route('/')
def index():
    return render_template('index.html',title='introduction')

@app.route('/index')
def indexx():
    return render_template('indexx.html',title='introductionn')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and validate_email(email):
            if password and len(password)>=6:
                try:
                    sess = getdb()
                    user = sess.query(User).filter_by(email=email,password=password).first()
                    if user:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        session['name'] = user.name
                        del sess
                        flash('login successfull','success')
                        return redirect('/info')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
    return render_template('login.html',title="login")

# email validation
def validate_email(email):
    if len(email) > 7:
        if re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$",email) != None:
            return True
        return False


@app.route('/signup',methods=['GET','POST'])
def signup():       
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if name and len(name) >= 3:
            if email and validate_email(email):
                if password and len(password)>=6:
                    if cpassword and cpassword == password:
                        try:
                            sess = getdb()
                            newuser = User(name=name,email=email,password=password)
                            sess.add(newuser)
                            sess.commit()
                            del sess
                            flash('registration successful','success')
                            return redirect('/login')
                        except Exception as e:
                            print('here',e)
                            flash('email account already exists','danger')
                    else:
                        flash('confirm password does not match','danger')
                else:
                    flash('password must be of 6 or more characters','danger')
            else:
                flash('invalid email','danger')
        else:
            flash('invalid name, must be 3 or more characters','danger')
    return render_template('signup.html',title='signup')

@app.route('/logout')
def logout():
    if session.get('isauth'):
        session.clear()
        flash('you have been logged out','warning')
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html',title='about')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        text = request.form.get('message','')
        file = request.files['file']
        if len(text) > 0:
            print(text)
            result = text_summarizer(text)
            session['result'] = result
            return redirect(url_for('summary', result=result))

        if 'file' in request.files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_type = filename.split('.')[-1]
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                sess = getdb()
                new_file = File(filename=filename,file_path = file_path, file_type = file_type, user_id = session['id'])
                sess.add(new_file)
                sess.commit()
                del sess
                flash('File Uploaded')

                if file_type in audio_type:
                    result = transcript(file_path)
                    return redirect(url_for('summary', summary=result ))
                elif file_type in video_type:
                    result = video_converter(file_path)
                elif file_type in document_type:
                    with open(file_path,'r') as f:
                        text = f.read()
                    result = text_summarizer(text)
                    session['result'] = result
                    return redirect(url_for('view_file', summary = result))
            
    return render_template('upload.html',title='upload')

@app.route('/summary')
def summary():
    if not session.get('isauth'):
        flash('please login first','danger')
        return redirect('/login')
    else:
        result=session['result']
        return render_template('summary.html',title='summary',summary=result)
    return render_template('summary.html',title='summary')
    

@app.route('/contact')
def contact():
    return render_template('contact.html',title='contact')

@app.route('/info')
def info():
    if not session.get('isauth'):
        flash('please login first','danger')
        return redirect('/login')
    else:
        try:
            db = getdb()
            user = db.query(User).filter_by(uid=session['id']).first()
            if user:
                name = user.name
                email = user.email
                file = db.query(File).filter_by(uid=session['id']).first()
                display_file = []
                if file:
                    file_name = file.filename
                    file_type = file.file_type
                    file_path = file.file_path
                    created_on = file.created_at
                    display_file.append((file_name,file_type,file_path,created_on))
                    return render_template('info.html',title='info',
                                           name=name,
                                           display_file=display_file)
        except:
            flash('please create profile first','danger')
    return render_template('profile_info.html',title='Profile Information')
                           
if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
