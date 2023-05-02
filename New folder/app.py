from flask import Flask, render_template
from flask import Flask, render_template, request, redirect
import plotly.express as px 
from database import Feedback
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine


app = Flask(__name__)
def load_data():
    df = px.data.iris()
    return df

def getdb():
    engine = create_engine('sqlite:///app.sqlite', echo=True)
    db = scoped_session(sessionmaker(bind=engine))
    return db



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if len(name) == 0 or len(message) == 0:
            print('Name or message is empty')
        else:
            db = getdb()
            db.add(Feedback(name=name, email=email, message=message))
            db.commit()
            db.close()
            return redirect('/feedback')
    return render_template('feedback.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)