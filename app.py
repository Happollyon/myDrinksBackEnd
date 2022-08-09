
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

#This function is used to create the tables 
def createTable(query):
    db.execute()
    db.commit()
    print('SUCCESS!')

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
        user = db.execute("INSERT INTO users(username,password) VALUES(:username,:password) returning id, username",{'username':username,'password':password}).fetchall()
        db.commit()
        return jsonify({'userData':[dict(row) for row in user]})



#This endpoint checks if the user is already registered. 
@app.route('/loggin/<string:username>/<string:password>',methods=['get'])
def loggin(username,password):
    user = db.execute("SELECT username,id FROM users WHERE username = :username AND password = :password",{'username':username,'password':password}).fetchall()
    db.commit()
    
    if user:
        return jsonify({'logged':'true','userData':[dict(row) for row in user]})
    else:
        return jsonify({'logged':'false'})
        


#this endpoint clears all rows from table
@app.route('/clearuserstable')
def clearuserstable():
    db.execute('DELETE FROM users WHERE id != 0') #deletes all the rows
    val= db.execute("SELECT * FROM users").fetchall()
    db.commit()

    return jsonify({'data':[dict(row) for row in val]})#returns empty object.  

@app.route('/likedrink/<int:user_id>/<int:drink_id>')
def likedrink(user_id,drink_id):
   #check if user alread likes the drink
   alreadyLiked = db.execute("SELECT * FROM user_favs WHERE user_id = :user_id AND drink_id = :drink_id",{'user_id':user_id,'drink_id':drink_id}).fetchall()
   db.commit()
   # if user already likes the drink end.
   if alreadyLiked:
       return jsonify({'alreadyLiked':'true'})
   else:
       db.execute('INSERT INTO user_favs(user_id,drink_id) VALUES(:user_id,:drink_id)',{'user_id':user_id,'drink_id':drink_id})
       db.commit()
       return jsonify({'successful':'true'})

# this endpoint returns all drinks liked by the user
@app.route('/selectliked/<int:user_id>')
def selectLiked(user_id):
    liked_drinks = db.execute("SELECT * FROM user_favs WHERE user_id = :user_id",{'user_id':user_id}).fetchall()
    db.commit()
    return jsonify({'successful':'true','liked_drinks':[dict(row) for row in liked_drinks]})

# this endpint return if user already likes the drink or not
@app.route('/liked/<int:user_id>/<int:drink_id>')
def liked(user_id,drink_id):
    #check if user already likes the drink
    alreadyLiked = db.execute("SELECT * FROM user_favs WHERE user_id = :user_id AND drink_id = :drink_id",{'user_id':user_id,'drink_id':drink_id}).fetchall()
    db.commit()
    
    if alreadyLiked:
        return jsonify({'alreadyLiked':'true'})
    else:
        return jsonify({'alreadyLiked':'false'})

# this endpoint removes liked drinks from user_favs table
@app.route('/dislike/<int:user_id>/<int:drink_id>')
def dislike(user_id,drink_id):
    db.execute("DELETE  FROM user_favs WHERE user_id = :user_id AND drink_id = :drink_id",{'user_id':user_id,'drink_id':drink_id})
    db.commit()

    return jsonify({'success':'true'})

if __name__ == '__main__':
	app.run(debug=True)
