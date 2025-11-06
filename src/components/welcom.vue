<template>
<div style="width: 100vw; height: 100vh; justify-content: center; display: flex; align-items: center; ">
    <div style="font-size: 30px;  display: flex; width: 40%; height: 25%; background-color: #F8FAFC; border-radius: 20px; border: 5px solid #E2E8F0; padding: 50px; align-items: center; justify-content: center; margin-bottom: 20%; flex-direction: column;" >
        
        <b><p style="text-align: center; margin-top: 50px; position: relative; top: 20px;" >Здравствуйте, пользователь! С помощью нашего финансового калькулятора вы сможете анализировать свои финансы, что позволяет экономить время. Все ваши данные удобно и безопасно хранятся в вашем аккаунте.</p></b>

        <button id="welcome-button" style="width: 100%; font-size: 30px; margin-bottom: 40px ; position: relative; top: -20px;" @click="handle">Создать первый расчет</button>

    </div>
    
</div>

</template>


<script>
import { useRouter } from 'vue-router';
export default{
    setup(){
        const router = useRouter()
        const handle = () => {
            router.push("/input")
        }
        
        return{handle}
    }
}
</script>

