<template>
  <div class="board-container">
    <header class="header">
      <h2>桌台看板</h2>
      <span>在线：服务员端</span>
    </header>
    
    <div class="grid">
      <!-- 循环渲染 20 个桌台 -->
      <div 
        v-for="i in 20" 
        :key="i" 
        class="table-card"
        :class="i === 15 ? 'busy' : 'free'"
      >
        <div class="table-name">Mesa {{ i.toString().padStart(2, '0') }}</div>
        <!-- 如果是 15 号桌，显示占用状态和金额，否则显示空闲 -->
        <div v-if="i === 15" class="table-info">
          <span>S/ 45.00</span>
          <span class="time">30 min</span>
        </div>
        <div v-else class="table-info">
          <span>Disponible</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.board-container {
  padding: 10px;
  background-color: #f3f4f6;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0 5px;
}

.grid {
  display: grid;
  /* 强约束 3 列，间距 10px */
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.table-card {
  padding: 15px 10px;
  border-radius: 8px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 90px; /* 严格控制高度，防面条化 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table-name {
  font-size: 18px;
  font-weight: bold;
}

.table-info {
  margin-top: 10px;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
}

/* 颜色状态 */
.free { background-color: #10b981; } /* 空闲绿 */
.busy { background-color: #ef4444; } /* 用餐红 */

.time {
  background-color: rgba(0,0,0,0.2);
  padding: 0 4px;
  border-radius: 4px;
}
</style>