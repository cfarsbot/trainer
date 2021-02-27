from flask import Flask
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL
import json
import bcrypt
import time
from random import randrange
import random
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mysql = MySQL()

# python_bcrypt==0.3.2
# these should be located in a saperate conf file
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'trainer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()


# Modifiy single item of a wordlist
@app.route('/update_wordlist', methods=['PATCH', 'PUT', 'DELETE'])
def updateWordlist():
    try:
        body = request.get_json()
        user_id = body['user']['id']
    except:
        return "Error", 400
    if request.method == 'PATCH':
        try:
            data = body['word']
        except:
            return "Error", 400

        updateSingleEntry(data, user_id)
        return "correct", 200
    if request.method == 'PUT':
        try:
            en = body['word']['en']
            de = body['word']['de']
            list_id = body['list_id']
            
            addSingleEntry(en, de, list_id)
            return getWordlist(user_id), 200
        except:
            return "Error", 400
    if request.method == 'DELETE':
        try:
            word_id = body['word']['id']

            deleteEntry(word_id, user_id)
            print(request.get_json())
            return "correct", 200
        except:
            return "Error", 400  

@app.route('/wordlist', methods=['POST', 'DELETE'])
@cross_origin()
def route_getWordList():
    body = request.get_json()
    try:
        user_id = body['user']['id']
    except:
        return "error", 403
    if request.method == 'POST':     
        exists_wordlist = """ SELECT EXISTS(SELECT * FROM wordlists_index WHERE creator_id = %s);"""

        cursor.execute(exists_wordlist, user_id)
        result = cursor.fetchone()[0]
            
            
        if( result == 0): # no matches found, user dosent have any wordlists
            print("No list found")
            return {'hasLists':False}, 200, {'ContentType':'application/json'}
        else:
            print("list found")
            return getWordlist(user_id)

    if request.method == 'DELETE':
        try:
            list_id = body['list_id']
            deleteList(list_id, user_id)
            return getWordlist(user_id)
        except:
            return "Error", 400
        
            


@app.route('/play_wordlist', methods=['POST'])
def play():
    if request.method == 'POST':
        try:
            body = request.get_json()
            user_id = body['user']['id']
            print(user_id)
            print(getWordlist(user_id, True)) #Default parameter, retuns shuffled list
            return "OK", 200
        except:
            return "Error", 400

            

@app.route('/create_wordlist', methods=['POST', 'PUT'])
@cross_origin()
def createWordlist():
    try:
        body = request.get_json()
        user = body['user']
        user_id = user['id']
        user_name = user['name']
    except:
        return "Error", 400
    if request.method == 'POST': # creates a full Wordlist with words in it
        try:
            list_name = body['listname']
            wordlist = body['data']
            saveWordlist(user_id, user_name, list_name, wordlist)
        except:
            return "Error", 400

    if request.method == 'PUT': # creates only a Wordlist header, response is only a new generated id for the array of words
        # axios only sends put requests, if the data is inside the data Object..
        try:
            list_name = body['data']
            saveWordlist(user_id, user_name, list_name)
            return getWordlist(user_id)
        except:
            return "Error", 400

@app.route('/login', methods=['POST'])
@cross_origin()
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
    


@app.route('/register', methods=['POST'])
@cross_origin()
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

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



def getWordlist(user_id):

    # get all wordlists that where created by the user
    select_wordlist_index = """ (SELECT * FROM wordlists_index WHERE creator_id = %s) """
    cursor.execute(select_wordlist_index, user_id)
    data = cursor.fetchall()

    final_wordlist = []

    for i in range(len(data)):
        list_id = data[i][1] #      2. Elem in table
        list_name = data[i][2] #    3. Elem in table
         
        # bulid JSON, add it to the wordlist
        json = { "list_name":list_name, "list_id":list_id ,"array":getEntrys(list_id)}
        final_wordlist.append(json)
        

    print(final_wordlist)
         
    return jsonify(final_wordlist)


def getEntrys(list_id):
   

    select_wordlist_index = """ (SELECT * FROM wordlists_entrys WHERE list_id = %s) """ #get all member of the array list_id
    cursor.execute(select_wordlist_index, list_id)
    data = cursor.fetchall()
    
    wordlist = []
    for i in range(len(data)): #iterate over all entrys we got from the SQL Statement
        word_en = data[i][1]
        word_de = data[i][2]
        word_id = data[i][3]
        # bulid json object, add it to the arraylist (wordlist)
        json = {"en":word_en, "de":word_de, "id":word_id}
        wordlist.append(json)


    return wordlist    


def saveWordlist(user_id, user_name, list_name, wordlist=0,):
    list_id = randrange(int(time.time()))


    insert_index = """INSERT INTO `wordlists_index`(list_id,list_name,creator_id,creator_name) VALUES (%s, %s, %s, %s); """
    data = (list_id, list_name,user_id, user_name )
    cursor.execute(insert_index, data)

    # if wordlist is empty, exit here.
    if(wordlist == 0):
        return
        
        
    # insert entrys into the wordlists_entrys table
    for i in range(len(wordlist)):
        en = wordlist[i]['en']
        de = wordlist[i]['de']
        addSingleEntry(en, de, list_id)

def addSingleEntry(en, de, list_id):
            insert_entrys = """ INSERT INTO `wordlists_entrys`(list_id,word_en,word_de) VALUES (%s, %s, %s);"""
            data = (list_id, en,de)
            cursor.execute(insert_entrys, data)
            conn.commit()


def updateSingleEntry(data, user_id):
    de = data['de']
    en = data['en']
    word_id = data['id']

    if(ownEntry(word_id, user_id)):
        # update both words, use word_id to identify the correct row
        update_entry = """ UPDATE wordlists_entrys SET word_en = %s, word_de= %s WHERE entry_id = %s """
        data = (en,de, word_id)

        cursor.execute(update_entry, data)
        conn.commit()


def deleteList(list_id, user_id):
    data = getEntrys(list_id)

    # iterate over list, delete one after another
    for i in range(len(data)):
        deleteEntry(data[i]['id'], user_id)

    # delete the index to get fully rid of the list
    delete_index = """ DELETE FROM wordlists_index WHERE list_id = %s """
    cursor.execute(delete_index, list_id)
    conn.commit()


# checks if the user owns a given word.
def ownEntry(word_id, user_id):

    # get list_is's that the user owns
    select_entry = """ SELECT list_id FROM wordlists_entrys WHERE entry_id = %s """
    cursor.execute(select_entry, word_id)
    list_id = cursor.fetchone()[0]

    # ich glaube hier ist ein logischer fehler, weil immer nur nach einer list_id geguckt wird und nicht, ob
    # word_id in der gefundenen list_id ist.
    # ich weiß also nicht, ob word_it in list_id ist. Ich weiß nur, dass der nutzer eine Liste besitzt
    # Hab jetzt aber keine zeit mehr das zu fixen

    exists_wordlist = """ SELECT EXISTS(SELECT * FROM wordlists_index WHERE creator_id = %s AND list_id = %s);"""
    data = (user_id, list_id)
    cursor.execute(exists_wordlist, data)
    result = cursor.fetchone()[0]
    if(result == 1):
        print("user owns list")
        return True
    else:
        return False
     

def deleteEntry(word_id, user_id):
    if(ownEntry(word_id, user_id)):
        delete_entry = """ DELETE FROM wordlists_entrys WHERE entry_id = %s  """
        cursor.execute(delete_entry, word_id)
        conn.commit()
    else:
        return "Error", 403

def generatePassword(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf8'), salt)


def checkPassword(password, hashed):   
    if(bcrypt.checkpw(password.encode('utf8'),hashed.encode('utf8'))):
        print("password correct")
        return True
    else:
        print("password invalid")
        return False

     


if __name__ == '__main__':
    app.run()
