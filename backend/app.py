from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from sqlalchemy import JSON
from dotenv import load_dotenv
import os

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

path_env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(path_env_file):
    load_dotenv(path_env_file)
    secret_key_env = os.getenv("SECRET_KEY")


class Users(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable = False )
    password = db.Column(db.String(255) ,nullable = False)
    incomes = db.Column(JSON, default = 0) 


class SignUp:
    
    @staticmethod
    def validation_password(some_password):
        dict_password_error = {
            "error" : False,
            "reson_errors" : []
        }
        digit_boolean = []
        alpha_boolean = []
        
        for letter in some_password:
            digit_boolean.append(letter.isdigit()) 
            alpha_boolean.append(letter.isalpha())
        
        if len(some_password) < 8:
            dict_password_error["error"] = True
            dict_password_error["reson_errors"].append("пароль должен быть больше или равен 8 символам")
        
        if not any(alpha_boolean):
            dict_password_error["error"] = True
            dict_password_error["reson_errors"].append("пароль должен содержать в себе буквы")

        if not any(digit_boolean):
            dict_password_error["error"] = True
            dict_password_error["reson_errors"].append("пароль должен содержать цифры")

        return dict_password_error
    
    @staticmethod
    def signup(data):
        login = data.get("login")
        password = data.get("password")
        captcha_token = data.get("token")
        dict_validate = SignUp.validation_password(some_password=password)

        if password and login and captcha_token:
            if not dict_validate["error"]:
                #отправляем в пост запросе (аунтефикация сервером по ключу и токену)
                dict = {
                    'secret' : secret_key_env,
                    'response' : captcha_token
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
                            #Хеширование пароля
                            hash_password = generate_password_hash(password)
                            user = Users(login=login, password=hash_password)
                            #Сохранение в бд
                            db.session.add(user)
                            db.session.commit()
                            return_data = {
                                "token_from_my_server" : user.id,
                                "authorization" : "True"
                            }
                            return jsonify(return_data)
                    else:
                        return jsonify({"authorization" : "False", "reason" : "Капча не пройдена"})

                except Exception as e:
                    print(f"ошибка {e}")
                    return jsonify({"authorization" : "False", "reason" : "Ошибка при запросе на сервере" })
            else:
                fstring = f"{', '.join(dict_validate['reson_errors'])} "
                return jsonify({ "authorization" : "False", "reason":  fstring  })
        else:
            return jsonify({ "authorization" : "False", "reason":  "заполните все поля"  }) 
            
    
        
 

class Login:
    @staticmethod
    def login(auth_data):
        auth_login = auth_data["auth_l"]
        auth_password = auth_data["auth_p"]


        if auth_login and auth_password:
            #Проверям есть ли пользователя в базе данных
            find_element_in_Users = Users.query.filter_by(login=auth_login).first()
            
            if find_element_in_Users and check_password_hash(find_element_in_Users.password, auth_password):
                return jsonify({'info_auth' : "True", 'token' : find_element_in_Users.id})
            else:
                return jsonify({'info_auth' : "False", "reason" : "такого пользователя не существует"})
        else:
            return jsonify({'info_auth' : "False", "reason" : "заполните все поля"})





#Регистрация!!!
@app.route('/signup_account', methods = ['POST'])
def signup():
    data = request.get_json()
    return SignUp.signup(data=data)

#Авторизация!!! 
@app.route("/login_account", methods = ["POST"])
def login():
    auth_data = request.get_json()
    return Login.login(auth_data=auth_data)
    
    
      
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
        except Exception as e:
            print("Ошибка на маршруте /analytics: {e}")
    
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
    except Exception as e:
        print(f"Ошибка на маршруте /analytics_page: {e}")


with app.app_context():
    db.create_all()  



if __name__ == "__main__":
    app.run(debug=True, port=5000)