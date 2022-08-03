from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://mesclvyfkornqx:0f7774e9362ac46a6aaf73a126b74a05903e0314d13ec45a66318e5528a252ab@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d2q7psbls4sks2'
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(16),unique = True)
	password = db.Column(db.String(16))


@app.route('/')
def index():
	
	return 'Hello, Flask!'

if __name__ == '__main__':
	app.run(debug=True)
