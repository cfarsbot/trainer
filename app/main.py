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
# these should be located in a saperate conf file
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'trainer'
app.config['MYSQL_DATABASE_HOST'] = 'mysql-server'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()
# Modifiy single item of a wordlist
@app.route('/update_wordlist', methods=['PATCH', 'PUT', 'DELETE'])
@cross_origin()
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


@app.route('/stats', methods=['POST'])
def stats():
    
        body = request.get_json()
        user_id = body['user']['id']

        if request.method == 'POST':
            select_meta = """ select list_id, list_name, count_correct, count_false FROM wordlists_index natural join wordlists_meta WHERE user_id = %s """
            cursor.execute(select_meta, user_id)
            result = cursor.fetchall()

            final = []
            for row in result:
                print(row)

                json = {"list_id":row[0], "list_name": row[1], "count_correct": row[2], "count_false": row[3]}
                final.append(json)
            
        return jsonify(final)

        
            


@app.route('/play_wordlist', methods=['POST'])
@cross_origin()
def play():
    try:
        body = request.get_json()
        user_id = body['user']['id']
        list_id = body['data']['list_id']
        lang = body['data']['selected_lang']
    except:
        return "error", 401

    if request.method == 'POST':
        return jsonify(getListByID(list_id, lang)), 200

@app.route('/validate_de', methods=['POST'])
@cross_origin()
def validate_de():
    try:
        body = request.get_json()
        words = body['words']
        user = body['user']
        user_id = user['id']
    except:
        return "error", 401
    if request.method == 'POST':
        print(user)
        print("Validate DE")
        validation = []

        idx_correct = 0
        idx_false = 0

        for word in words:
            toCheck = word
            # get array of the correct word
            correct = getWordByID(toCheck['id'])
            solution = correct[2] # correct[1] = german word returned from DB
            if(word['de'] == solution): # userinput is correct
                print("correct")
                json = {'de':word['de'], 'en':word['en'], 'id':word['id'], 'result':True}
                validation.append(json)
                idx_correct += 1
            if(word['de'] != solution): # userinput isn't correct
                print("wrong")
                json = {'de':word['de'], 'en':word['en'], 'id':word['id'], 'result':False}
                validation.append(json)
                idx_false += 1
    updateUserStats(user, idx_correct, idx_false)
    createMetaData(user_id,list_id, idx_correct, idx_false)

        
    return jsonify(validation), 200

@app.route('/validate_en', methods=['POST'])
@cross_origin()
def validate_en():
    try:
        body = request.get_json()
        words = body['words']
        user = body['user']
        user_id = user['id']
        list_id = body['list_id']
    except:
        return "error", 401
    if request.method == 'POST':
        print(body)
        print("Validate EN")
        validation = []

        idx_correct = 0
        idx_false = 0

        for word in words:
            toCheck = word
            # get array of the correct word
            correct = getWordByID(toCheck['id'])
            solution = correct[1]
            # correct[1] = english word returned from DB
            if(word['en'] == solution): # userinput is correct
                print("correct")
                json = {'de':word['de'], 'en':word['en'], 'id':word['id'], 'result':True}
                validation.append(json)
                idx_correct += 1
            if(word['en'] != solution): # userinput isn't correct
                print("wrong")
                json = {'de':word['de'], 'en':word['en'], 'id':word['id'], 'result':False}
                validation.append(json)
                idx_false += 1
    updateUserStats(user, idx_correct, idx_false)                
    createMetaData(user_id,list_id, idx_correct, idx_false)
        
    return jsonify(validation), 200
            

@app.route('/create_wordlist', methods=['POST', 'PUT'])
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


    

def createMetaData(user_id, list_id, idx_correct, idx_false):

    exists_wordlist = """ SELECT EXISTS(SELECT * FROM wordlists_meta WHERE list_id = %s);"""
    cursor.execute(exists_wordlist, list_id)
    result = cursor.fetchone()[0]
    if( result == 0): #no list found
        print("no list found, updating")
        insert_meta = """INSERT INTO wordlists_meta (user_id,list_id,count_correct,count_false) VALUES (%s, %s, %s, %s); """
        data = (user_id, list_id, idx_correct, idx_false)
        cursor.execute(insert_meta, data)
        conn.commit()
    else: #list found, update existing
        print("Wordlist exists, updating")
        update_stats = """ UPDATE wordlists_meta SET count_correct = %s, count_false= %s WHERE list_id = %s """
        data = (idx_correct, idx_false, list_id)
        cursor.execute(update_stats, data)
        conn.commit()



def getWordByID(word_id):
    select_word = """ SELECT * FROM wordlists_entrys WHERE entry_id = %s """
    cursor.execute(select_word, word_id)
    result = cursor.fetchall()[0]
    return result

def updateUserStats(user,idx_correct, idx_false):
    print(user)
    user_id = user['id']
    currentCorrect = user['Count_Correct']
    currentFalse = user['Count_False']
    update_stats = """ UPDATE user SET Count_Correct = %s, Count_False= %s WHERE id = %s """
    data = (currentCorrect + idx_correct, currentFalse + idx_false, user_id)
    cursor.execute(update_stats, data)
    conn.commit()


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
        json = { "list_name":list_name, "list_id":list_id ,"array":getListByID(list_id)}
        final_wordlist.append(json)
        

    print(final_wordlist)
         
    return jsonify(final_wordlist)


def getListByID(list_id, lang=None):
   
    selected_lang = "*"
    if(lang != None):
        if(lang == 0):
            select_wordlist_index = """ (SELECT word_de, entry_id FROM wordlists_entrys WHERE list_id = %s) """
            cursor.execute(select_wordlist_index, list_id)
            result = cursor.fetchall()

            wordlist = []
            for i in range(len(result)): #iterate over all entrys we got from the SQL Statement
                word_de = result[i][0]
                word_id = result[i][1]
                # bulid json object, add it to the arraylist (wordlist)
                json = {"de":word_de, "id":word_id}
                wordlist.append(json)
            return wordlist    


        if(lang == 1):
            select_wordlist_index = """ (SELECT word_en, entry_id FROM wordlists_entrys WHERE list_id = %s) """ 
            cursor.execute(select_wordlist_index, list_id)
            result = cursor.fetchall()

            wordlist = []
            for i in range(len(result)): #iterate over all entrys we got from the SQL Statement
                word_en = result[i][0]
                word_id = result[i][1]
                # bulid json object, add it to the arraylist (wordlist)
                json = {"en":word_en, "id":word_id}
                wordlist.append(json)
            return wordlist  
    else:
        select_wordlist_index = """ (SELECT * FROM wordlists_entrys WHERE list_id = %s) """ 

        cursor.execute(select_wordlist_index, list_id)
        result = cursor.fetchall()
            
        wordlist = []
        for i in range(len(result)): #iterate over all entrys we got from the SQL Statement
            word_en = result[i][1]
            word_de = result[i][2]
            word_id = result[i][3]
            # bulid json object, add it to the arraylist (wordlist)
            json = {"de":word_de, "en":word_en, "id":word_id}
            wordlist.append(json)
        return wordlist  


@app.route('/login', methods=["POST"])
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


@app.route('/register', methods=["POST"])
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
    data = getListByID(list_id)

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


     


if __name__ == '__main__':
    app.run()
