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

ALLOWED_EXTENSIONS = ['txt','pdf','wav','mp3', 'mp4', 'doc','docx', 'mov' , 'wmv', 'flv', 'avi' 'mkv', 'webm' ]

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
                        return redirect('/profile')
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
            return redirect(url_for('view_file', name='summary', file_type='text'))

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
                with open(file_path,'r') as f:
                    text = f.read()
                result = text_summarizer(text)
                session['result'] = result
                return redirect(url_for('view_file', name=filename, file_type=file_type))
    return render_template('upload.html',title='upload')

@app.route('/view_file/<name>/<file_type>')
def view_file(name,file_type):
    if name == 'summary':
        return render_template('view_file.html',title='view_file',name=name,file_type=file_type,result=session['result'])
    else:
        return render_template('view_file.html',title='view_file',name=name,file_type=file_type, result=session['result'])

@app.route('/profile',methods=['GET','POST'])
def profile():
    if not session.get('isauth'):
        flash('please login first','danger')
        return redirect('/login')
    if request.method == 'POST':
        contact = request.form.get('contact')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        if len(contact) == 0 or len(gender) == 0 or len(dob) == 0:
            flash('please fill all the fields','danger')
            return redirect('/profile')
        db = getdb()
        profile = db.query(Profile).filter_by(uid=session['id']).first()
        if profile is not None:
            profile.contact = contact
            profile.dob = dob
            profile.gender = gender
            db.commit()
            db.close()
            flash('profile updated','success')
            return redirect('/info')
        else:
            profile = Profile(uid=session['id'], contact=contact, gender=gender, dob=dob)
            db.add(profile)
            db.commit()
            db.close()
            flash('profile created','success')
            return redirect('/profile')
    try:
        db = getdb()
        print('uid',session['id'])
        profile = db.query(Profile).filter_by(uid=session['id']).first()
        if profile is not None:
            return render_template('profile.html',title='profile', profile=profile)
        else:
            return render_template('profile.html',title='profile')
    except:
        return render_template('profile.html',title='profile')
    

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
                profile = db.query(Profile).filter_by(uid=session['id']).first()
                return render_template('profile_info.html',
                                title='Profile Information',
                                profile=profile, user=user)
            else:
                return render_template('profile_info.html',title='Profile Information')
        except:
            flash('please create profile first','danger')
    return render_template('profile_info.html',title='Profile Information')
                           
                           

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
