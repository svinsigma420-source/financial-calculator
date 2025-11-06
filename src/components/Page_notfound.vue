<template>
    <div class="error-container">
        <div class="error-message">Ошибка. Ничего не найдено по этому пути</div>
        <button class="home-button" @click="handleClick">Перейти на главную страницу</button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()
const handleClick = () => {
    router.push({name: "input_data"})
}
</script>

<style scoped>

</style>