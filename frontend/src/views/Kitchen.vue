<template>
  <div class="kitchen-container">
    <header class="header">
      <h1>Cocina - 厨房看板</h1>
      <span>待出餐: {{ tickets.length }} 单</span>
    </header>

    <div v-if="tickets.length === 0" class="empty">
      暂无待出餐订单...
    </div>

    <div class="ticket-list">
      <div v-for="ticket in tickets" :key="ticket.ticket_id" class="ticket-card">
        <div class="ticket-header">
          <span class="table-num">Mesa {{ ticket.table_id.toString().padStart(2, '0') }}</span>
          <span class="batch">批次: {{ ticket.batch_id }}</span>
        </div>
        
        <div class="items">
          <div v-for="(item, index) in ticket.items" :key="index" class="item">
            <div class="item-main">
              <span class="qty">{{ item.quantity }}x</span>
              <span class="name">{{ item.name_es }}</span>
            </div>
            <!-- 备注必须用显眼的红色高亮出来 -->
            <div v-if="item.remarks" class="remark">
              >> {{ item.remarks }} <<
            </div>
          </div>
        </div>

        <button class="complete-btn" @click="completeTicket(ticket.ticket_id)">
          已出餐 (Completado)
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const tickets = ref([])
let timer = null

// 注意这里写死了你电脑的局域网 IP 或者用 window.location.hostname
const hostname = window.location.hostname
const API_BASE = `http://${hostname}:8000/api`

// 拉取订单
const fetchTickets = async () => {
  try {
    const res = await fetch(`${API_BASE}/kitchen/tickets`)
    const data = await res.json()
    
    // 如果有新订单进来，这里还可以加声音提示
    if (data.length > tickets.value.length) {
      // playSound() // 后面再搞
    }
    tickets.value = data
  } catch (e) {
    console.error('拉取厨房订单失败', e)
  }
}

// 标记出餐
const completeTicket = async (id) => {
  try {
    await fetch(`${API_BASE}/kitchen/tickets/${id}/complete`, { method: 'POST' })
    fetchTickets() // 刷新列表
  } catch (e) {
    alert('操作失败')
  }
}

// 开始轮询（每 3 秒拉一次）
onMounted(() => {
  fetchTickets()
  timer = setInterval(fetchTickets, 3000)
})

// 离开页面时清除定时器
onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
/* 厨房看板：高对比度，大字，无废话 */
.kitchen-container { background: #1a1a1a; min-height: 100vh; color: white; padding: 15px; }
.header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 15px; }
.header h1 { font-size: 24px; margin: 0; color: #fff; }

.empty { text-align: center; font-size: 20px; color: #666; margin-top: 50px; }

.ticket-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }

.ticket-card { background: #fff; color: #000; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; }
.ticket-header { background: #fbbf24; padding: 10px; display: flex; justify-content: space-between; font-weight: bold; font-size: 20px; }
.batch { font-size: 16px; }

.items { padding: 15px; flex-grow: 1; }
.item { margin-bottom: 15px; border-bottom: 1px dashed #ccc; padding-bottom: 10px; }
.item-main { display: flex; gap: 10px; font-size: 22px; font-weight: bold; }
.qty { color: #ef4444; }
.remark { margin-top: 5px; color: #ef4444; font-size: 18px; font-weight: bold; }

.complete-btn { width: 100%; padding: 20px; background: #10b981; color: white; border: none; font-size: 22px; font-weight: bold; cursor: pointer; }
.complete-btn:active { background: #059669; }
</style>