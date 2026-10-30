<template>
  <div class="order-container">
    <!-- 顶部固定头 -->
    <header class="header">
      <button @click="goBack" class="back-btn"> < 返回 </button>
      <h2>Mesa {{ tableId }}</h2>
      <span>已点: {{ cartCount }}</span>
    </header>

    <!-- Tag 分类栏 -->
    <div class="tag-bar">
      <span 
        v-for="tag in availableTags" 
        :key="tag"
        class="tag-item"
        :class="{ active: selectedTags.includes(tag) }"
        @click="toggleTag(tag)"
      >
        {{ tag }}
      </span>
    </div>
    
    <!-- 极简列表区 -->
    <div class="menu-list">
      <div 
        v-for="dish in filteredMenu" 
        :key="dish.id" 
        class="dish-item"
        @click="openSheet(dish)"
      >
        <div class="dish-info">
          <div class="dish-name">{{ dish.name_es }}</div>
          <div class="dish-zh">{{ dish.name_zh }}</div>
        </div>
        <div class="dish-action">
          <span class="price">S/ {{ dish.price.toFixed(2) }}</span>
        </div>
      </div>
    </div>

    <!-- 底部唯一主操作按钮 -->
    <div class="bottom-bar">
      <button class="submit-btn" @click="submitOrder">发送至厨房 ({{ cartCount }})</button>
    </div>

    <!-- ======= 底部弹出面板 (Bottom Sheet) ======= -->
    <!-- 遮罩层 -->
    <div class="overlay" v-if="showSheet" @click="closeSheet"></div>
    
    <!-- 面板内容 -->
    <div class="bottom-sheet" :class="{ 'show': showSheet }" v-if="activeDish">
      <div class="sheet-header">
        <h3>{{ activeDish.name_es }}</h3>
        <span>S/ {{ (activeDish.price * activeQuantity).toFixed(2) }}</span>
      </div>

      <!-- 数量加减 -->
      <div class="quantity-control">
        <button class="qty-btn" @click="activeQuantity > 1 ? activeQuantity-- : null"> - </button>
        <span class="qty-num">{{ activeQuantity }}</span>
        <button class="qty-btn" @click="activeQuantity++"> + </button>
      </div>

      <!-- 快捷备注标签 -->
      <div class="remark-section">
        <div class="remark-title">快捷备注 (Opciones):</div>
        <div class="remark-tags">
          <span 
            v-for="remark in quickRemarks" 
            :key="remark"
            class="remark-tag"
            :class="{ active: selectedRemarks.includes(remark) }"
            @click="toggleRemark(remark)"
          >
            {{ remark }}
          </span>
        </div>
      </div>

      <!-- 确认加入 -->
      <button class="confirm-btn" @click="confirmAdd">加入订单 (Agregar)</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchMenu } from '../api/index.js'
import { submitOrderApi } from '../api/index.js'

const route = useRoute()
const router = useRouter()
const tableId = route.params.id

const menu = ref([])
const selectedTags = ref([])
const allTags = ['招牌', '炒饭', '炒面', '热菜', '鸡肉', '牛肉', '猪肉', '主食', '饮料']

// 购物车数据
const cart = ref([])
const cartCount = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))

// Bottom Sheet 状态
const showSheet = ref(false)
const activeDish = ref(null)
const activeQuantity = ref(1)
const quickRemarks = ['微辣', '中辣', '打包', '不要葱', '少盐']
const selectedRemarks = ref([])

const filteredMenu = computed(() => {
  if (selectedTags.value.length === 0) return menu.value
  return menu.value.filter(dish => 
    selectedTags.value.every(tag => dish.tags.includes(tag))
  )
})
const availableTags = allTags

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) selectedTags.value.splice(index, 1)
  else selectedTags.value.push(tag)
}

// 打开弹窗
const openSheet = (dish) => {
  activeDish.value = dish
  activeQuantity.value = 1
  selectedRemarks.value = []
  showSheet.value = true
}

// 关闭弹窗
const closeSheet = () => {
  showSheet.value = false
  setTimeout(() => { activeDish.value = null }, 300) // 等待动画结束
}

// 切换备注
const toggleRemark = (remark) => {
  const index = selectedRemarks.value.indexOf(remark)
  if (index > -1) selectedRemarks.value.splice(index, 1)
  else selectedRemarks.value.push(remark)
}

// 确认加入购物车
const confirmAdd = () => {
  cart.value.push({
    dish: activeDish.value,
    quantity: activeQuantity.value,
    remarks: [...selectedRemarks.value]
  })
  closeSheet()
}

const submitOrder = async () => {
  // 1. 测试点击是否生效
  alert("按钮已点击，准备发送...") 

  if (cart.value.length === 0) {
    alert("购物车是空的！")
    return
  }
  
  // 组装发给后端的数据
  const orderData = {
    table_id: parseInt(tableId),
    submit_id: Date.now().toString() + Math.random().toString(36).substring(2), // 兼容性写法
    items: cart.value.map(item => ({
      dish_id: item.dish.id,
      name_es: item.dish.name_es,
      quantity: item.quantity,
      remarks: item.remarks
    }))
  }

  try {
    // 2. 测试网络请求是否发得出去
    alert("正在连接后端...") 
    await submitOrderApi(orderData)
    
    alert(`发送成功！已通知厨房并存入数据库。`)
    cart.value = [] 
    router.push('/') 
  } catch (error) {
    // 3. 捕获网络错误（比如连不上后端）
    alert("提交失败: " + error.message)
    console.error(error)
  }
}

const goBack = () => { router.push('/') }

onMounted(async () => {
  try {
    menu.value = await fetchMenu()
  } catch (error) {
    alert("菜单加载失败: " + error.message)
  }
})
</script>

<style scoped>
.order-container { 
    height: 100vh; 
    display: flex; 
    flex-direction: column; 
    background-color: #f8f9fa; 
}

.header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 10px; 
  background: #fff; 
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
  flex: 0 0 auto; 
  z-index: 10; 
}

/* 新增：强制桌号变黑加粗 */
.header h2 {
  color: #111;
  font-weight: 700;
  font-size: 20px;
}
.back-btn { 
    background: none; 
    border: none; font-size: 
    16px; color: #3b82f6; 
}

.tag-bar { 
    display: flex; 
    overflow-x: auto; 
    white-space: nowrap; 
    padding: 10px; 
    background: #fff; 
    border-bottom: 1px solid #eee; 
    flex: 0 0 auto; gap: 8px; 
    scrollbar-width: none; 
}

.tag-bar::-webkit-scrollbar { 
    display: none; 
}

.tag-item { 
  padding: 6px 12px; 
  background: #f1f1f1; 
  border-radius: 16px; 
  font-size: 14px; 
  color: #333; /* 加深颜色 */
  font-weight: 500;
  cursor: pointer; 
}

.tag-item.active { background: #3b82f6; color: white; }
.menu-list { flex: 1 1 auto; overflow-y: auto; padding: 10px; padding-bottom: 80px; }
.dish-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background: #fff; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); cursor: pointer; }
.dish-name { font-size: 16px; font-weight: bold; color: #333; }
.dish-zh { font-size: 12px; color: #888; margin-top: 4px; }
.dish-action { display: flex; align-items: center; gap: 15px; }
.price { font-size: 18px; color: #ef4444; font-weight: bold; }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 10px; background: #fff; box-shadow: 0 -2px 10px rgba(0,0,0,0.05); z-index: 10; }
.submit-btn { width: 100%; padding: 15px; background: #10b981; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; }

/* ====== 弹窗样式 ====== */
.overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 20; }
.bottom-sheet {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: #fff; border-radius: 16px 16px 0 0;
  padding: 20px; z-index: 30;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  box-shadow: 0 -4px 15px rgba(0,0,0,0.1);
}
.bottom-sheet.show { transform: translateY(0); }
.sheet-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.sheet-header h3 { margin: 0; font-size: 18px; }
.sheet-header span { font-size: 18px; color: #ef4444; font-weight: bold; }

.quantity-control { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px; }
.qty-btn { 
  width: 40px; 
  height: 40px; 
  border-radius: 50%; 
  border: 1px solid #ccc; 
  background: #fff; /* 改成纯白背景 */
  color: #333; /* 强制文字为深色 */
  font-size: 24px; /* 字体再大一点 */
  font-weight: bold; /* 加粗 */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer; 
  user-select: none;
}
/* 增加按下的反馈，防止误触 */
.qty-btn:active {
  background: #eee;
}
.qty-num { font-size: 20px; font-weight: bold; min-width: 30px; text-align: center; }

.remark-section { margin-bottom: 20px; }
.remark-title { font-size: 14px; color: #666; margin-bottom: 10px; }
.remark-tags { display: flex; flex-wrap: wrap; gap: 10px; }
.remark-tag { padding: 8px 16px; border-radius: 20px; background: #f1f1f1; font-size: 14px; cursor: pointer; }
.remark-tag.active { background: #10b981; color: white; }

.confirm-btn { width: 100%; padding: 15px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; }
</style>