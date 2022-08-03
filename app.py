from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import uri

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =uri 
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(16),unique = True)
	password = db.Column(db.String(16))


@app.route('/')
def index():
	
	return 'Hello, Flask!'

@app.route('/register')
def register():
	db.engine.execute("insert into Users(unsername,password) values('fagner','fagner123');")
	
	for record in db.engine.execute('SELECT * FROM Users;'):
		print(record)


if __name__ == '__main__':
	app.run(debug=True)
