from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint

budget = 17000

user0={
    "id":"0",
    "name":"Olena",
    "salary":"2000",
    "phone":"+380930472937",
    "credits":["0"]
}
user1={
    "id":"1",
    "name":"Rick",
    "salary":"2000",
    "phone":"+380930472937",
    "credits":["1","2"]
}
credit0 = {
    "id" : "0",
    "date" : "12.10.2018",
    "money" : "2000",
    "status" : "activity"
}
credit1 = {
    "id" : "1",
    "date" : "12.02.2019",
    "money" : "3000",
    "status" : "activity"
}
credit2 = {
    "id" : "2",
    "date" : "23.04.2018",
    "money" : "5000",
    "status" : "activity"
}
users = [user0,user1]
credits = [credit0,credit1,credit2]

budget-=int(credit0['money'])
budget-=int(credit1['money'])
budget-=int(credit2['money'])
# Init app
app = Flask(__name__)


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
    if 0<=int(user_id)<len(users):
        return jsonify(users[int(user_id)]["credits"])
    else:
        return make_response(jsonify('user id not found'), 404)


@app.route('/users/', methods=['GET'])
def get_all_user():
    id_all_user = []
    for i in range(len(users)):
        id_all_user.append(str(i))
    return jsonify(id_all_user)


@app.route('/users/', methods=['POST'])
def create_user():
        user = {
            'id': str(len(users)),
            'name': request.json['name'],
            'salary': request.json['salary'],
            'phone': request.json['phone'],
            'credits': []
        }
        users.append(user)
        return jsonify(len(users)-1)

#  CREDIT
@app.route('/credits/', methods=['GET'])
def get_all_credit():
    id_all_credit = []
    for i in range(len(credits)):
        id_all_credit.append(str(i))
    return jsonify(id_all_credit)


@app.route('/credits/<credit_id>', methods=['GET'])
def get_credit(credit_id):
    if 0 <= int(credit_id) < len(credits):
        return jsonify(credits[int(credit_id)])
    else:
        return make_response(jsonify('user id not found'), 404)


@app.route('/credits/<user_id>', methods=['POST'])
def post_credit(user_id):
    if 0 <= int(user_id) < len(users):
        if int(users[int(user_id)]["salary"])*5<int(request.json['money']):
            return make_response(jsonify('too small salary'), 500)
        if int(request.json['money'])<100:
            return make_response(jsonify('too little credit'), 500)
        if budget>=float(request.json['money']):
            money = float(request.json['money'])*0.3+float(request.json['money'])
            credit = {
                'id': str(len(credits)),
                'date': request.json['date'],
                'money': str(money),
                'status' : "activity"
            }
            global budget
            budget-=float(request.json['money'])
            users[int(user_id)]['credits'].append(str(len(credits)))
            credits.append(credit)
            return jsonify(len(credits)-1)
        else:
            return make_response(jsonify('too much credit'), 500)
    else:
        return make_response(jsonify('user id not found'), 404)


@app.route('/credits/<credit_id>', methods=['PUT'])
def put_credit(credit_id):
    m = budget+float(credits[int(credit_id)]['money'])
    if 0 <= int(credit_id) < len(credits):
        if int(request.json['money']) < 100:
                return make_response(jsonify('too little credit'), 500)
        if  m >= int(request.json['money']):
            global budget
            budget+=float(credits[int(credit_id)]['money'])
            money = float(request.json['money'])*0.3+float(request.json['money'])
            credits[int(credit_id)]['date']=request.json['date']
            credits[int(credit_id)]['money'] = str(money)
            budget-=float(request.json['money'])
            return jsonify(credits[int(credit_id)])
    else:
        return make_response(jsonify('credit id not found'), 404)


@app.route('/credits/<credit_id>', methods=['DELETE'])
def delete_credit(credit_id):
    if credits[int(credit_id)]['status']=="ending":
        return make_response(jsonify('already change'), 500)
    if 0 <= int(credit_id) < len(credits):
        credits[int(credit_id)]['status']="ending"
        global budget
        budget+=float(credits[int(credit_id)]['money'])
        return jsonify(credits[int(credit_id)])
    else:
        return make_response(jsonify('credit id not found'), 404)


if __name__ == '__main__':
    app.run(debug=True)
