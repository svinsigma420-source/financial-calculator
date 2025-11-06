<template>
    <!--Главный div аутификации-->
        <div style="display: flex; width: 600px; height: 500px; background-color: #F8FAFC; border-radius: 15px;  align-items: center; flex-direction: column; border: 5px solid #E2E8F0;">
        
        <h1>Поле входа в аккаунт✅</h1>
        <div style="margin: 40px;  " >
            <label style="font-size: 25px;" >Логин: </label>
            <input type="text" placeholder="Введите логин" v-model="auth_login"  style="height: 32px; border-radius: 4px; font-size: 20px; position: relative; right: -6px; margin-left: 5px" >
        </div>
        <div >
            <label style="font-size: 25px;">Пароль: </label>
            <input type="password" placeholder="Введите пароль" v-model="auth_password"  style="height: 30px; border-radius: 4px; font-size: 20px; margin-left: 5px; " >
        </div>
        
       
        <div style="gap: 15px; display: flex; position: relative; top: 30px;">
            <button class="some-button" @click="login" >Войти</button>
            <button class="some-button" @click="resetFunc">Отмена</button>
        </div>

        
</div>


</template>

<script>
import {ref, watch} from "vue"
export default{
    setup(){
       
        const resetFunc = () => {
            auth_login.value = ""
            auth_password.value = ""
        }
        const error = ref("")
        watch(error, (newValue) => {
            if(!error.value){
                null
            }else{
                alert(newValue)
                error.value = ""
            }

        })
        
        const login = async () => {
            if(localStorage.getItem("token") === null){
                     if( auth_login.value && auth_password.value){
                try{
                    //Составляем запрос 
                    const auth_obj = {
                        "auth_l" : auth_login.value,
                        "auth_p" : auth_password.value
                    }
                   
                    const response = await fetch('http://localhost:5000/login_account', {
                        method: 'POST',
                        headers : {"Content-Type" : "application/json"},
                        body : JSON.stringify(auth_obj)
                    })


                    //Обрабатываем возвращенные данные
                    const data = await response.json()
                    
                    //Проверка авторизации с капчей
                    if (data["info_auth"] == "True"){
                        localStorage.setItem("token" , data["token"] )
                        alert("Вы успешно зашли в ранее созданный аккаунт")

                    }
                    else{
                        alert(`Ошибка: ${data["reason"]}`)
                    }
                    
                }catch(err){
                    console.error(err)
                }
            }else{ 
                error.value = "Заполните все поля"
                        }
                }else{
                    alert("Сначала выйдите из текущего аккаунта, чтобы создать или войти в другой.")
                        }
            resetFunc()
        }
        
        const auth_login = ref("")
        const auth_password = ref("")
        return{auth_login, auth_password, resetFunc, login}
    }
}




</script>

<style scoped>
.some-button:first-of-type {
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
