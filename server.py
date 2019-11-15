from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_mysqldb import MySQL

budget = 57000

# Init app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'lab7'

mysql = MySQL(app)

""" swagger specific """
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "test"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

#  USER
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    cur = mysql.connection.cursor()
    credit = user_credit=cur.execute("SELECT credit FROM users WHERE id = %s",(user_id,))
    if credit!=1:
        return make_response(jsonify('user id not found'), 404)    
    credit = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    
    credit = str(credit)[4:-5]
    print(credit)
    list =[]
    for el in credit.split():
	list.append(el)
    print(list)
    return jsonify(list)


@app.route('/users/', methods=['GET'])
def get_all_user():
    cur = mysql.connection.cursor()
    id_all = user_credit=cur.execute("SELECT id FROM users")
    id_all = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    print(id_all)
    id_all = str(id_all)[2:-3]
    print(id_all)
    list =[]
    for el in id_all.split(',), ('):
	list.append(el)
    print(list)
    return jsonify(list)


@app.route('/users/', methods=['POST'])
def create_user():
       
	name = request.json['name']
	salary = request.json['salary']
	phone = request.json['phone']
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO users( name,salary,phone,credit) VALUES( %s, %s, %s ,%s)",(name, salary,phone,""))

	user_id=cur.execute("select MAX(id) from users")
	user_id = str(cur.fetchall())
	user_id = user_id[2:-4]

	mysql.connection.commit()
	cur.close()
   
        return user_id

#  CREDIT
@app.route('/credits/', methods=['GET'])
def get_all_credit():
    cur = mysql.connection.cursor()
    id_all_credit = user_credit=cur.execute("SELECT credit FROM users")
    id_all_credit = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    id_all_credit = str(id_all_credit)[4:-5]
    list =[]
    for el in id_all_credit.split():
	list.append(el)
    print(list)
    return jsonify(list)


@app.route('/credits/<credit_id>', methods=['GET'])
def get_credit(credit_id):
    cur = mysql.connection.cursor()
    credit = user_credit=cur.execute("SELECT * FROM credit WHERE id = %s",(credit_id,))
    if credit!=1:
        return make_response(jsonify('credit id not found'), 404)    
    credit = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    
    credit = str(credit)[2:-3]
    print(credit)
    list =[]
    for el in credit.split(", u"):
	list.append(el)
    print(list)
    return jsonify(list)



@app.route('/credits/<user_id>', methods=['POST'])
def post_credit(user_id):
        if int(request.json['money'])<100:
            return make_response(jsonify('too little credit'), 500)
        if budget>=float(request.json['money']):
            money = float(request.json['money'])*0.3+float(request.json['money'])

            global budget
            budget-=float(request.json['money'])

	    date = request.json['date']
	    money = request.json['money']
	    status = "activity"
	    cur = mysql.connection.cursor()
	    cur.execute("INSERT INTO credit(date,money,status) VALUES(%s, %s, %s)",(date, money,status))
	    

	    credit_id=cur.execute("select MAX(id) from credit")
	    credit_id = str(cur.fetchall())
	    credit_id = credit_id[2:-4]
 
	    user_credit=cur.execute("SELECT credit FROM users WHERE id = %s",(user_id,))
	    if user_credit!=1:
		return make_response(jsonify('user id not found'), 404)
	   
	    user_credit = cur.fetchall()

	    if user_credit == ((None,),):
		user_credit = ""
		user_credit =  str(credit_id)
	    else:
		user_credit = str(user_credit)
		user_credit = user_credit[4:-5]
		print(user_credit)
		user_credit = str(user_credit)+ " " + str(credit_id)
	    
	    cur.execute("UPDATE users SET credit = %s WHERE id = %s",(user_credit,user_id))	
	   
	    mysql.connection.commit()
	    cur.close()
		
	    
            return credit_id
        else:
            return make_response(jsonify('too much credit'), 500)
    
        


@app.route('/credits/<credit_id>', methods=['PUT'])
def put_credit(credit_id):
    cur = mysql.connection.cursor()
    money = cur.execute('SELECT money FROM credit WHERE id = %s',(credit_id,))
    if money !=1:
            return make_response(jsonify('credit not find'), 404)
    money= str(cur.fetchall())[4:-5]
    print(money)
    global budget
    budget+=int(money)
    if int(request.json['money'])<100:
            return make_response(jsonify('too little credit'), 500)
    if budget>=float(request.json['money']):
            money = float(request.json['money'])*0.3+float(request.json['money'])

            
            budget-=float(request.json['money'])
        
	    date = request.json['date']
	    money = request.json['money']
	    cur.execute("UPDATE credit SET date = %s,money = %s WHERE id = %s",(date,money,credit_id))
	    

	    credit_id=cur.execute("select MAX(id) from credit")
	    credit_id = str(cur.fetchall())
	    credit_id = credit_id[2:-4]
 
	    

	    mysql.connection.commit()
	    cur.close()
		
	    
            return credit_id
    else:
            return make_response(jsonify('too much credit'), 500)


@app.route('/credits/<credit_id>', methods=['DELETE'])
def delete_credit(credit_id):
    cur = mysql.connection.cursor()
    status = cur.execute("SELECT status FROM credit WHERE id = %s",(credit_id,))
    if status!=1:
        return make_response(jsonify('credit id not found'), 404)    
    status = str(cur.fetchall())[4:-5]
    if status != 'activity':
	return make_response(jsonify('yet'), 500)
    cur.execute('UPDATE credit SET status = "ending" WHERE id = %s',(credit_id,)) 
    money = cur.execute('SELECT money FROM credit WHERE id = %s',(credit_id,))
    money= str(cur.fetchall())[4:-5]
    print(money)
    global budget
    budget+=int(money)
    mysql.connection.commit()
    cur.close()
    print(status)
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
