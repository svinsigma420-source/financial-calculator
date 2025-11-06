<template>
  <div class="buttons-container">
    <button 
      v-for="(category, index) in categories" 
      :key="index"
      :class="{ active: category === props.selected_category_props}"
      @click="select(index)"
    >
      {{ category }}
    </button>
  </div>
</template>

<script>

export default {
  props:{
    selected_category_props:{
      required: true,
      type: String,
    }
  },
  emits: ["select"],
  setup(props, {emit}) {
    const categories = (["Еда", "Жилье", "Одежда", "Транспорт", "Развлечения", "Образование", "Другое"])
    
    const select = (index) => {
      emit("select", categories[index]  ) 
    }
    
    return { categories, select, props}
  }
}
</script>

<style scoped>
.buttons-container {
  display: flex;
  justify-content: space-around;
  width: 90%; 
  padding: 10px; 
  background: #f5f5f5; 
  border-radius: 15px
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background: #e0e0e0;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
}

button.active {
  background: #42b983;
  color: white;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
</style>