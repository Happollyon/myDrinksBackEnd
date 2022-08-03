import imp
from flask import Flask, jsonify
from sqlalchemy import create_engine, false
from sqlalchemy.orm import scoped_session,sessionmaker
import os


app = Flask(__name__)
app.config.update(dict(
    DEBUG = True
))
engine = create_engine('postgresql://dmcjgfxxlzkwzz:54d357220eb56acc5bc27a98ace88fdc63a94a6837378d415896997085118fcf@ec2-52-19-188-149.eu-west-1.compute.amazonaws.com:5432/d48equ8fqv99ao')

db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
	
	return 'Hello, Flask!'


@app.route('/register/<string:username>/<string:password>',methods=['GET'])
def register(username,password):
	usernameCheck = db.execute("SELECT * FROM users WHERE username = :username",{'username':username}).fetchone()
	db.commit()
	if usernameCheck:
		return{'available':'false'}
	else:
		db.execute("INSERT INTO users(username,password) VALUES(:username,:password)",{'username':username,'password':password})
		val= db.execute("SELECT * FROM users").fetchall()
		db.commit()
	
		return jsonify({'data':[dict(row) for row in val]})

if __name__ == '__main__':
	app.run(debug=True)
