import { createRouter, createWebHistory } from 'vue-router'
import TableBoard from './views/TableBoard.vue'
import OrderMenu from './views/OrderMenu.vue'

const routes = [
  { path: '/', name: 'TableBoard', component: TableBoard },
  { path: '/order/:id', name: 'OrderMenu', component: OrderMenu },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router