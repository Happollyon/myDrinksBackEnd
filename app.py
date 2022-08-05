
"""
    @author Fagner Nunes 
    July 2022
    github => https://github.com/Happollyon
"""
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import os


app = Flask(__name__)

#creating engine using my db uri -> prosgesql hosted on HEROKU
engine = create_engine('postgresql://dmcjgfxxlzkwzz:54d357220eb56acc5bc27a98ace88fdc63a94a6837378d415896997085118fcf@ec2-52-19-188-149.eu-west-1.compute.amazonaws.com:5432/d48equ8fqv99ao')

db = scoped_session(sessionmaker(bind=engine))

#index page
@app.route('/')
def index():	
	return 'Hello, Flask!'


# this end point checks if the username is available
@app.route('/checkusername/<string:username>',methods=['GET'])
def checkusername(username):
    usernameCheck = db.execute("SELECT * FROM users WHERE username = :username",{'username':username}).fetchone()
    db.commit()
    if usernameCheck: #if there is a username returns false 
        return{'available':'false'}
    else:
        return{'available':'true'}

@app.route('/register/<string:username>/<string:password>',methods=['GET'])
def register(username,password):
    usernameCheck = db.execute("SELECT * FROM users WHERE username = :username",{'username':username}).fetchone()
    db.commit()

    if usernameCheck:
        #a sencond username is check for safety  
        return{'available':'false'}
    else:
        #If username is available user is inserted to database
        db.execute("INSERT INTO users(username,password) VALUES(:username,:password)",{'username':username,'password':password})
        val= db.execute("SELECT * FROM users").fetchall()
        db.commit()
        return jsonify({'data':[dict(row) for row in val]})



#This endpoint checks if the user is already registered. 
@app.route('/loggin/<string:username>/<string:password>',methods=['get'])
def loggin(username,password):
    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",{'username':username,'password':password}).fetchone()
    db.commit()
    
    if user:
        return jsonify({'logged':'true','username':user['username']})
    else:
        return jsonify({'logged':'false'})
        


#this endpoint clears all rows from table
@app.route('/clearuserstable')
def clearuserstable():
    db.execute('DELETE FROM users WHERE id != 0') #deletes all the rows
    val= db.execute("SELECT * FROM users").fetchall()
    db.commit()

    return jsonify({'data':[dict(row) for row in val]})#returns empty object.  


if __name__ == '__main__':
	app.run(debug=True)
