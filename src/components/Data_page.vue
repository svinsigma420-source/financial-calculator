<template>
  <div >
    <!-- Корневой див -->
    <div class="main_part" >

      
      <!-- Логотип и заголовок сайта -->
      <div class="div_logo" style="display: flex; justify-content: center; position: relative; top: -50px;" >
        <h1 style="margin-bottom: 5px;">Денежный калькулятор</h1>
      </div>
      <h2 style="margin-top: 5px; position: relative; right: -180px; position: relative; top: -50px;"  >Финансовое приложение для анализа денежных средств</h2>
      
      <!-- Основа для расходов и доходов (белое поле) -->
      <div style=" position: relative; top: -50px;  display: flex; width: 800px; height: 530px; background-color: #F8FAFC; border-radius: 20px; border: 5px solid #E2E8F0; padding: 30px; flex-direction: column; gap: 20px;">

        <!-- Основной див доходов -->
        <div style="display: flex; background-color: #38A169; width: 100%; height: 250px; border-radius: 15px; align-items: center; flex-direction: column;">
          <h2 style="color: white;">Доходы:</h2>
          
          <!-- Поле ввода доходов -->
          <div style="margin: 10px;">
            <label style="color: #BEE3F8; font-weight: bold;">Добавить доходы </label>
            <input type="number" style="color: black; background-color: white; border: 2px solid #2C5282; border-radius: 5px; padding: 5px;" placeholder="зарплата..." v-model="pay" @keyup.enter="add_pay">
          </div>

          <!-- Список доходов -->
          <div style="width: 600px; height: 130px; background-color: #F8FAFC; overflow-y: auto; margin: 10px; border-radius: 10px; padding: 7px; border: 3px solid #2C5282">
             <p v-if="array_pay == false" style="text-align: center;" > Пусто, добавте доходы<span style="color:blue"> (не больше десяти миллионов и не меньше тысячи рублей)</span></p>
            <div v-for="(el, index) in array_pay" :key="index" style="color: black; margin-right: 10px; background-color: #BEE3F8; text-align: center; border-radius: 5px; margin: 10px; padding: 5px;">
              <label style="color: #2C5282; font-weight: bold;">Доход номер {{ index + 1 }} : </label> {{ el }} ₽
               <button @click="delete_pay(index) "  class="delete_btn" style="float: right; position: relative; top: -2px; background-color: #2C5282; color: white; ">Удалить доход</button>
            </div>
          </div>
          
        </div>
        
        <!-- Основной див расходов -->
        <div style="display: flex; background-color: #E53E3E; width: 100%; height: 250px; border-radius: 15px; align-items: center; flex-direction: column;">
          <h2 style="color: white;">Расходы:</h2>
          
          <!--Кнопки категорий-->
          <Buttons @select="select" :selected_category_props="select_categoty" />

          <!-- Поле ввода расходов -->
          <div style="margin: 5px;">
            <label style="color: #FED7D7; font-weight: bold;">Добавить расход </label>
            <input type="number" style="color: black; background-color: white; border: 2px solid #9B2C2C; border-radius: 5px; padding: 5px;" placeholder="расход..." @keyup.enter="add_spends" v-model="input">
          </div>
          <!-- Список расходов -->
          <div style="width: 600px; height: 130px; background-color: #F8FAFC; overflow-y: auto; margin: 10px; border-radius: 10px; padding: 7px; border: 3px solid #9B2C2C">
            <p v-if="array_spend == false" style="text-align: center;" > Пусто, добавте расходы<span style="color:blue"> (не больше десяти миллионов и не меньше тысячи рублей)</span></p>
            <div v-for="(el, index) in array_spend" :key="index" style="color: black; margin-right: 10px; background-color: #FED7D7; text-align: center; border-radius: 5px; margin: 10px; padding: 5px;">
              <label style="color: #9B2C2C; font-weight: bold;">#{{el.category}} Расход номер {{ index + 1 }} : </label> {{ el.value }} ₽
              <button @click="delete_spend(index) "  class="delete_btn" style="float: right; position: relative; top: -2px; ">Удалить расход</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted} from "vue"
import Buttons from "./Buttons.vue"
import {useDataStore} from "./Store"
import { storeToRefs } from 'pinia' // Импортируем storeToRefs

export default {
  components: {Buttons},
  
  setup() {  
    const store = useDataStore()
    
    const { 
      pay,
      array_pay,
      array_spend,
      input,
      select_categoty
    } = storeToRefs(store)
    
    
    
    onMounted( async () => {
      console.log("data page mounted")
      try{
        const token = localStorage.getItem("token")
        if (token){
          const response = await fetch("http://localhost:5000/analytics_page", {
          method: "POST",
          headers : {"Content-type" : 'application/json', "Authorization": `Bearer ${localStorage.getItem("token")}`}
        })
        
      const data = await response.json()
      if(response.ok && data["incomes"] && data["expenses"]){
        array_pay.value = data["incomes"]
        array_spend.value = data["expenses"]
      }
      }
      
      }catch(err){
        console.error(`ошибка ${err}`)
      }
    })

    
    const {
      add_pay,
      add_spends,
      delete_pay,
      delete_spend,
      select
    } = store

    return { 
      pay,
      array_pay,
      array_spend,
      input,
      select_categoty,
      add_pay,
      add_spends,
      delete_pay,
      delete_spend,
      select
    }


    
    

    
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=WDXL+Lubrifont+JP+N&display=swap');

*{
  color: #2D3748;
  font-family: "WDXL Lubrifont JP N", sans-serif;
  font-weight: 400;
  font-style: normal;
}
</style>