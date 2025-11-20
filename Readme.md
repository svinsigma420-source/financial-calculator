Financial Management App
Full-stack веб-приложение для управления личными финансами с аналитикой расходов и доходов.
 
Функциональность:
1) Авторизация и регистрация с reCAPTCHA
2) Учет доходов и расходов  
3) Визуализация финансовой аналитики
4) Безопасное хранение данных

Технологии
Backend: Python, Flask, SQLAlchemy, SQLite  
Frontend: Vue 3, Pinia, Vue Router, Vite


Быстрый старт:

cd backend
pip install -r requirements.txt
python run.py

cd frontend
npm install
npm run dev



ВАЖНО ЗАМЕНИТЬ YOUR_SITE_KEY(создать файл config.js и экспортировать из него ваш сайт-ключ:

export const config = {"SITE-KEY" : "PUT_KEY"}) 

И YOUR_SECRET_KEY(создать файл с названием .env и написать:

SECRET_KEY=PUT_SECRET_KEY

) 


на ваши валдиные ключи полученные на официальном сайте https://developers.google.com/recaptcha?hl=en(Вид капчи: reCAPTCHA v2 "I'm not a robot")
