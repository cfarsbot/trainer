from flask import Blueprint
from flask import Flask
from flask import request
from flask import jsonify

import bcrypt    

auth = Blueprint('auth', __name__)
from main import conn, cursor

@auth.route('/hello')
def hello():
    return "hello"


@auth.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        try:
            body = request.get_json()
            email = body['user']['email']
            password = body['user']['password']

            exists_email = """ SELECT EXISTS(SELECT * from user WHERE email = %s);"""
            cursor.execute(exists_email, email)
            result = cursor.fetchone()[0]        
    
            if(result == 1): # if user exits....
                del(result)

                # find user with given email and get his id
                select_user_id = """ (SELECT `id` FROM user WHERE email =%s);"""
                cursor.execute(select_user_id, email)
                user_id = cursor.fetchone()[0]
            
                # get with id the password hash
                select_credentials = """ (SELECT password FROM credentials WHERE id = %s);"""
                cursor.execute(select_credentials, user_id)
                credentials = cursor.fetchone()[0]

                # if password is valid
                if(checkPassword(password, credentials)):
                    # get user entry and bulid it to a JSON Object
                    select_user = """ (SELECT * FROM user WHERE id = %s); """
                    cursor.execute(select_user, user_id)
                    result = cursor.fetchall()[0]
                    user = []

                    for col in result:
                        user.append(col)

                    # user[5] (id) should be encrypted because it is used in request bodys to identify the user
                    user_json = {"email":user[0], "name":user[1], "Lang_DE":user[2], "Count_Correct":user[3], "Count_False":user[4], "id":user[5]}
                    return user_json, 200, {'ContentType':'application/json'}
                
                else:
                    return {'login':False}, 403, {'ContentType':'application/json'}
             
            else:
                return {'login':False}, 403, {'ContentType':'application/json'}
        except:
            return "Error", 400     

def checkPassword(password, hashed):   
    if(bcrypt.checkpw(password.encode('utf8'),hashed.encode('utf8'))):
        print("password correct")
        return True
    else:
        print("password invalid")
        return False


@auth.route('/register', methods=["POST"])
def register():
    try:
        body = request.get_json()
        email = body['user']['email']
        password = body['user']['password']
        name = body['user']['name']
    except:
        return "Error", 400

    if request.method == 'POST':
        # checks if the given E-Mail is already used
        exists_email = """ SELECT EXISTS(SELECT * from user WHERE email = %s);"""
       
        cursor.execute(exists_email, email)
        result = cursor.fetchone()[0]

        if(result == 1): # email exists already, cant register with that
            print("user exists!")
            return json.dumps({'success':False}), 403, {'ContentType':'application/json'} 
        else: # email isnt used

            print("user dosent Exists!")
            # generate salted password hash
            credentials = generatePassword(password)

            # put userdata into the user Table
            insert_user = """INSERT INTO `user` (email,Name,Lang_DE,Count_Correct,Count_False)VALUES (%s, %s, %s, %s, %s);"""
            data = (email, name, 0, 0 ,0)
            cursor.execute(insert_user, data)
            conn.commit()
            del(data)

            # get the generated user_id
            get_id = """ (SELECT `id` FROM user WHERE email = %s);"""
            cursor.execute(get_id, email)
            user_id = cursor.fetchone()[0]

            # put credentials in DB, user_id is primary
            insert_credentials = """ INSERT INTO `credentials` VALUES (%s, %s);"""
            data = (credentials,user_id)
            cursor.execute(insert_credentials, data)
            conn.commit()
            del(data)

        return ({'success':True}), 200, {'ContentType':'application/json'} 



def generatePassword(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf8'), salt)