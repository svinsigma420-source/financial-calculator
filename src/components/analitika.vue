<template>
<!--Главынй див-->
<div >
    <!--Первая часть аналитики-->
    <div style=" margin: 70px ; background-color: #F8FAFC; border-radius: 20px; padding: 20px; ">
        <div class="analytical_data">ДОХОДЫ: {{ sum_incomes }} </div> 
        <div class="analytical_data">РАСХОДЫ: {{ sum_expenses }}</div> 
        <div class="analytical_data">
            <span v-if="profit > 0">ПРИБЫЛЬ: {{ profit }}</span>
            <span v-else>УБЫТОК: {{ profit }}</span>
        </div>
        <div class="analytical_data">МАКСИМАЛЬНЫЙ РАСХОД: {{ max_spend }} </div>
        <div class="analytical_data">МАКСИМАЛЬНЫЙ ДОХОД: {{ max_pay }} </div>
        <div v-if="max_category !== 'Нет данных' "    class="analytical_data">САМАЯ ЗАТРАТНАЯ КАТЕГОРИЯ {{ max_category["category"] }} : {{ max_category["value"] }}  </div>
        <div v-else class="analytical_data">САМАЯ ЗАТРАТНАЯ КАТЕГОРИЯ: НЕТ ДАННЫХ</div>
        <div class="analytical_data">ОПЕРАЦИЙ ПО ДОХОДАМ: {{ amount_incomes }} </div>
        <div class="analytical_data">ОПЕРАЦИЙ ПО РАСХОДАМ: {{ amount_expenses }}</div>
    </div>
        
</div>


</template>


<script>
import {ref, onMounted, computed} from "vue"
import { useDataStore } from "./Store";
import { storeToRefs } from "pinia";
export default{
    setup(){
        
        const store = useDataStore()
        const {array_pay, array_spend} = storeToRefs(store)
        const array_all_spends = ref([])
        const array_all_pays = ref([])
        
        const sum_expenses = ref(0)
        const sum_incomes = ref(0)
        onMounted(async()=> {
            try{
                if(localStorage.getItem("token") !== null ){
                    const response = await fetch("http://localhost:5000/analytics_page", {
                    method: "POST",
                    headers: {"Content-Type" : "application/json", "Authorization" : `Bearer ${localStorage.getItem("token")}`}
                })
            const data = await response.json()
            
            if (Array.isArray(data.incomes) && Array.isArray(data.expenses)){
                for(var element of data["incomes"]){
                    sum_incomes.value += element
                    array_all_pays.value.push(element)
                }

                for(var element of data["expenses"]){
                    sum_expenses.value += element["value"]
                    array_all_spends.value.push(element["value"])
                }
            } else {
                console.error(`С сервера приходит не массив, а ${data["expenses"]} и ${data["incomes"]}`)
            }

        } else {
            for(var element of array_pay.value){
                sum_incomes.value += element
                array_all_pays.value.push(element)
            }

            for(var element of array_spend.value){
                sum_expenses.value += element.value
                array_all_spends.value.push(element["value"])
            }
        }

            }catch(err){
                console.error(`ошибка в analitka.vue ${err}`)
            }
        }
    )

    const profit = computed(() => {
        return sum_incomes.value - sum_expenses.value
    })


    const amount_incomes = computed(()=>{
        return store.array_pay.length
    })


    const amount_expenses = computed(()=>{
        return store.array_spend.length
    })

    const max_spend = computed(()=>{
        if(array_all_spends.value && array_all_spends.value.length > 0){
            return Math.max(...array_all_spends.value)
        }else{
            return 0
        }
        
    })

    const max_pay = computed(()=> {
        if(array_all_pays.value && array_all_pays.value.length > 0){
            return Math.max(...array_all_pays.value)
        }else{
            return 0
        }
    })

    const max_category = computed(() => {
        const spend_food = ref(0)
        const spend_live = ref(0)
        const spend_wear = ref(0)
        const spend_transport = ref(0)
        const spend_entertainment = ref(0)
        const spend_study = ref(0)
        const spend_other = ref(0)
        
        
        if(array_spend.value.length > 0){
            for(var element of array_spend.value)
            // (["Еда", "Жилье", "Одежда", "Транспорт", "Развлечения", "Образование", "Другое"])
            switch(element["category"]){
                case "Еда": spend_food.value += element.value; break
                case "Жилье":spend_live.value += element.value; break
                case "Одежда":spend_wear.value += element.value; break
                case "Транспорт":spend_transport.value += element.value; break
                case "Развлечения": spend_entertainment.value += element.value; break
                case "Образование": spend_study.value += element.value; break
                case "Другое": spend_other.value += element.value; break
                
            }
        

            const category_value_array = [
        {"category" : "Еда", "value" : spend_food.value},
        {"category" : "Жилье", "value" : spend_live.value},
        {"category" : "Одежда", "value" : spend_wear.value},
        {"category" : "Транспорт", "value" : spend_transport.value},
        {"category" : "Развлечения", "value" : spend_entertainment.value},
        {"category" : "Образование", "value" : spend_study.value},
        {"category" : "Другое", "value" : spend_other.value}
    ]

        
    
    
        const array_all_category = [spend_food.value, spend_live.value, spend_wear.value,spend_transport.value,spend_entertainment.value,spend_study.value,spend_other.value]
        const max_category_value = Math.max(...array_all_category)
        const index = array_all_category.indexOf(max_category_value)

        return { "category" : category_value_array[index]["category"].toUpperCase(), "value" : category_value_array[index]["value"] }


        }else{
            return "Нет данных"
        }
        
        


    })

        
       
        return{ sum_incomes, sum_expenses, profit, amount_expenses, amount_incomes, max_spend, max_pay, max_category}
    }
}

</script>