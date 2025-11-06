
import { defineStore } from "pinia";
import {ref, watch} from "vue"

export const useDataStore = defineStore("data", () => {
    //данные для списка расходов
    const input = ref(0)
    const array_spend = ref([])
    
    const removeIsState = false
    const removeToken = () =>{
      const state_localStorage = ref(localStorage.getItem("token") === null)
      if(state_localStorage.value !== true){
        localStorage.removeItem("token")
        array_pay.value = []
        array_spend.value = []
        select_categoty.value = ""
        removeIsState.value = true

      }
    }
    
    
    //функция отвечающая за список расходов
    const error = ref("")
    const add_spends = () => {
      if(input.value != false && input.value <= 10000000 && input.value >= 1000) {
        if(select_categoty.value == false){ 
          error.value = "Выберите категорию"
        }else{ array_spend.value.push(
          {
          value : input.value, 
          category : select_categoty.value
        }
      )
        error.value = ""
        input.value = ""}
        
       
      }else{
        error.value = ""
      }
    }

    watch(array_spend, async (newArray) => {
      //Запрос к серверу(сохраняем масив расходов в бд в виде json-строки)
      if(localStorage.getItem("token") !== null){
        fetch('http://localhost:5000/analytics', {
        method : "POST",
        headers: {"Content-Type" : "application/json", "Authorization" : `Bearer ${localStorage.getItem("token")}`},
        body : JSON.stringify({"expenses_array" : newArray})
      }) 
      }else if(first_notification.value === false){
        alert("Без входа в аккаунт данные не будут сохранены")
        first_notification.value = true
      }
    },  
    
    {deep: true})















    //данные для списка доходов
    const pay = ref(0)
    const array_pay = ref([])
        
    //функция отвечающая за список доходов
    const add_pay = () => {
      if(pay.value != false && pay.value <= 10000000 && pay.value >= 1000) {
        array_pay.value.push(pay.value)
        
        pay.value = ""
      }
    }

    const first_notification = ref(false)

    watch(array_pay, async (newArray) => {
      //Запрос к серверу(сохраняем масив доходов в бд в виде json-строки)
      if(localStorage.getItem("token") !== null){
        fetch('http://localhost:5000/analytics', {
        method : "POST",
        headers: {"Content-Type" : "application/json", "Authorization" : `Bearer ${localStorage.getItem("token")}`},
        body : JSON.stringify({"incomes_array" : newArray})
      }) 
      }else if(first_notification.value === false){
        alert("Без входа в аккаунт данные не будут сохранены")
        first_notification.value = true
      }
    },  
    
    {deep: true})




    //Функция отвечающая за категории кнопок
    const select_categoty = ref("")
    const select = (button) => {
      select_categoty.value = button
    }

    //Функции для удаления расходов и доходов
    const delete_spend = (index) => {
      array_spend.value.splice(index, 1)
    }
    const delete_pay = (index) => {
      array_pay.value.splice(index, 1)
    }



    
    return { pay, add_pay, input, array_spend, add_spends, array_pay, select, select_categoty , delete_spend, error, delete_pay, removeToken}}
  
  )