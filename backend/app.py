from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from sqlalchemy import JSON

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(16), nullable = False )
    password = db.Column(db.String(16) ,nullable = False)
    incomes = db.Column(JSON, default = 0)
    expenses = db.Column(JSON, default = 0)



#Регистрация!!!
@app.route('/signup_account', methods = ['POST'])
def signup():
    #парсим
    data = request.get_json()
    login = data["login"]
    password = data["password"]    
    token = data["token"]
    
    #отправляем в пост запросе (аунтефикация сервером по ключу и токена)
    dict = {
        'secret' : 'YOUR-SECRET-KEY',
        'response' : token
    }
    try:
        response = requests.post("https://www.google.com/recaptcha/api/siteverify",data=dict)
        response.raise_for_status()
        json_success_data = response.json()
        success_data = json_success_data.get("success", False)

        if success_data:
            #Проверка на существующий аккаунт
            user_valid = Users.query.filter_by(login=login).first()

            if user_valid:
                return jsonify({"authorization" : "False", "reason" : "Такой пользователь уже существует"})
            else:
                user = Users(login=login, password=password)
                db.session.add(user)
                db.session.commit()
                return_data = {
                    "token_from_my_server" : user.id,
                    "authorization" : "True"
                }
                return jsonify(return_data)
        else:
            return jsonify({"authorization" : "False", "reason" : "Капча не пройдена"})

    except:
        return jsonify({"authorization" : "False", "reason" : "Ошибка при запросе на сервере" })
        

#Авторизация!!!
@app.route("/login_account", methods = ["POST"])
def login():
    #Парсим
    auth_data = request.get_json()
    auth_login = auth_data["auth_l"]
    auth_password = auth_data["auth_p"]


    #Проверям есть ли пользователя в базе данных
    find_element_in_Users = Users.query.filter_by(login=auth_login).first()
    if find_element_in_Users and find_element_in_Users.password == auth_password:
        return jsonify({'info_auth' : "True", 'token' : find_element_in_Users.id})
    else:
        return jsonify({'info_auth' : "False", "reason" : "Такого пользователя не существует"})

      
@app.route("/analytics" , methods = ["POST"])
def analytics():
        try:
            analytics_data = request.get_json()
            analytics_token = request.headers.get("Authorization").split(" ")[1]
            user = Users.query.filter_by(id=analytics_token).first()
            
            if "incomes_array" in analytics_data and analytics_token:
                user.incomes = analytics_data["incomes_array"]
            elif analytics_token:
                user.expenses = analytics_data["expenses_array"]

            db.session.commit()
            print("Данные успешно записанны в бд")
        except:
            print("Ошибка на маршруте /analytics")
    
@app.route("/analytics_page" , methods = ["POST"])
def analytics_page():
    try:
        token_analytics_page = request.headers.get("Authorization").split(" ")[1]
        user = Users.query.filter_by(id=token_analytics_page).first() 
        if token_analytics_page:
            return jsonify({
                "incomes" : user.incomes,
                "expenses" : user.expenses
        })
    except:
        print("Ошибка на маршруте /analytics_page")


with app.app_context():
    db.create_all()  



if __name__ == "__main__":
    app.run(debug=True, port=5000)