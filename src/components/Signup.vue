<template>

<!--Главный div регстрации-->
<div style="display: flex; width: 600px; height: 500px; background-color: #F8FAFC; border-radius: 15px;  align-items: center; flex-direction: column; border: 5px solid #E2E8F0;">
    <h1>Поле регистрации✅</h1>
        <div style="margin: 40px; " >
            <label style="font-size: 25px;" >Логин: </label>
            <input type="text" placeholder="Введите логин" v-model="userLogin"   style="height: 32px; border-radius: 4px; font-size: 20px; position: relative; right: -6px; margin-left: 5px" >
        </div>
        <div >
            <label style="font-size: 25px;">Пароль: </label>
            <input type="password" placeholder="Введите пароль" v-model="userPassword"   style="height: 30px; border-radius: 4px; font-size: 20px; margin-left: 5px; " >
        </div>
        
        <div  v-show="state" class="g-recaptcha" id="renderThere" style="margin: 30px;"></div>
        <div v-show="!state" style="margin: 30px; font-size: 20px;"> Капча загружается⌛</div>
       
        <div style="gap: 15px; display: flex; position: relative; top: -30px;">
            <button class="some-button" @click="signupFunc" >Зарегистрироваться</button>
            <button class="some-button" @click="resetFunc" >Отмена</button>
        </div>

        
</div>
</template>


<script>
import { ref, watch, onMounted } from 'vue';
import { useDataStore } from './Store';
import { config } from '/config.js';
export default{
    setup(){
        const store = useDataStore()


        const saveToken = (token) =>{
            localStorage.setItem("token" , token)
        }
        

        
        
        
        const state = ref(false)
        const error = ref("")
        const userLogin = ref("")
        const userPassword = ref("")
        const resetFunc = () => {
            userLogin.value = ""
            userPassword.value = ""
        }
        
        watch(error, (newValue) => {
            if(!error.value){
                null
            }else{
                alert(newValue)
                error.value = ""
            }

        })

        onMounted(() => {
            
            grecaptcha.ready(() => {
                const element = document.querySelector("#renderThere")
                grecaptcha.render(element, {
                sitekey: config['SITE-KEY']
            })
            })

            setTimeout(() => {
                state.value = true
            }, 1000)
        })
        const data_finally = ref('')

        const signupFunc = async () => {
            const token = grecaptcha.getResponse()
            if(localStorage.getItem("token") === null){     
                try{
                    const obj = {
                        "token" : token,
                        "login" : userLogin.value,
                        "password" : userPassword.value
                    }
                    const response = await fetch('http://localhost:5000/signup_account', {
                        method: 'POST',
                        headers : {"Content-Type" : "application/json"},
                        body : JSON.stringify(obj)
                    })
                    const data = await response.json()
                    if (data["authorization"] === "True" && response.ok){
                        alert("Регистрация прошла успешно")
                        saveToken(data["token_from_my_server"])
                        store.saveChangeToken()
                        
                    }else{
                        alert(`Ошибка: ${data["reason"]}`)
                    }
                    
                }catch(err){
                    console.error(err)
                }
                }else{
                    alert("Сначала выйдите из текущего аккаунта, чтобы создать или войти в другой.")
                }
        
            resetFunc()
            grecaptcha.reset()
            }

        return{userLogin, userPassword, resetFunc, signupFunc, data_finally, state}
    }
}



</script>























<style>
.some-button:first-of-type, #welcome-button {
    margin-top: 50px; width: 150px; height: 40px; font-size: 17px; background-color: #2563EB; color: white; border-radius: 15px; cursor: pointer;
}
.some-button:last-of-type {
    margin-top: 50px; width: 150px; height: 40px; font-size: 17px; background-color: #94A3B8; color: white; border-radius: 15px; cursor: pointer;
}


.some-button:first-of-type:hover{
    background-color: #1D4ED8; 
    transition: background-color 0.2s;
}

.some-button:last-of-type:hover{
     background-color: #64748B; 
    transition: background-color 0.2s;
}



</style>

