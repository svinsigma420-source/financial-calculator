<template>
      <div style=" display: flex; background-color: rgb(128, 128, 128); justify-content: center; align-items: center; ">
        <div style="float: left;">
        <button @click="handleClick(1)"  class="blue-button">Ввод данных</button>
        <button @click="handleClick(2)"  class="blue-button">Аналитика</button>
        </div>
      </div>
      <div style="display: flex; justify-content: center; gap: 12px ; position: relative; right: -35%;" >
        <button @click="handleClick(3)"  class="blue-button" style="background-color: rgb(120, 200, 175); position: relative; ; top: -85px;">Регистрация</button>
      <button @click="handleClick(4)"  class="blue-button" style="background-color: rgb(120, 200, 175); position: relative; ; top: -85px;">Вход в аккаунт</button>
      <button class="blue-button" style="background-color: rgb(120, 200, 175); position: relative; ; top: -85px;" @click="store.removeToken">Выход</button>

      </div>

      
      <div style="display: flex; justify-content: center;">
        <RouterView></RouterView>
      </div>
   

    
</template>


<script>

import { useRouter } from "vue-router"
import { useDataStore } from "./components/Store";
import { onMounted, ref } from "vue";

export default{
  setup(){
    const store = useDataStore()
    
    onMounted( async () => {
      console.log("app mounted")
      try{
        const token = ref(localStorage.getItem("token"))
        if (token.value !== null || false ){
          const response = await fetch("http://localhost:5000/analytics_page", {
          method: "POST",
          headers : {"Content-type" : 'application/json', "Authorization": `Bearer ${localStorage.getItem("token")}`}
        })
        
      const data = await response.json()
      store.array_pay = data["incomes"]
      store.array_spend = data["expenses"]
      }
        
      
      }catch(err){
        console.error(`ошибка ${err}`)
      }
    })
    
    //Роутинг
    const router = useRouter()
    const handleClick = (number) => {
  const routes = {
    1: "input_data",
    2: "analytics", 
    3 : "signup",
    4 : "login"
  }
  const name_route = routes[number]
  router.push({name: name_route})
}
    
    return{handleClick, store}
  }
}

</script>


<style>


</style>