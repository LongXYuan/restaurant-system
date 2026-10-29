<template>
  <div class="board-container">
    <header class="header">
      <h2>桌台看板</h2>
      <span>在线：服务员端</span>
    </header>
    
    <div v-if="loading" class="loading">加载桌台数据中...</div>
    
    <div v-else class="grid">
      <!-- 循环渲染后端传来的真实桌台 -->
      <div 
        v-for="table in tables" 
        :key="table.id" 
        class="table-card"
        :class="table.status"
      >
        <!-- 显示西语桌号 -->
        <div class="table-name">{{ table.name_es }}</div>
        
        <div class="table-info">
          <span v-if="table.status === 'busy'">S/ {{ table.amount.toFixed(2) }}</span>
          <span v-else>Disponible</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchTables } from './api/index.js'

const tables = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    tables.value = await fetchTables()
  } catch (error) {
    alert(error.message)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* 样式和之前一样保持不变 */
.board-container { padding: 10px; background-color: #f3f4f6; min-height: 100vh; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 5px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.table-card { padding: 15px 10px; border-radius: 8px; color: white; display: flex; flex-direction: column; justify-content: space-between; min-height: 90px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.table-name { font-size: 18px; font-weight: bold; }
.table-info { margin-top: 10px; font-size: 14px; display: flex; justify-content: space-between; }
.free { background-color: #10b981; }
.busy { background-color: #ef4444; }
.loading { text-align: center; padding: 50px; font-size: 20px; color: #666; }
</style>