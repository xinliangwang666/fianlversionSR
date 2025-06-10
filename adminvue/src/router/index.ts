import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login',// 根路径重定向到登录页
  },
  {
    path: '/login',
    name: 'login',// 登录页面
    component: () => import('@/views/login/LoginView.vue'),
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/home/HomeView.vue'),
    redirect: '/home/dish',// 首页默认重定向到菜品管理
    // 设置二级路由
    children: [
      {
        path: '',
        name: 'dish',
        redirect: '/home/dish',   // 1. 菜品管理模块
      },
      {  // 2. 用户管理模块
        path: 'user',
        name: 'user',
        redirect: '/home/user/list',
        children: [
          {
            path: 'list',
            name: 'user-list',
            component: () =>
              import('@/views/home/homeChildren/user/UserView.vue'),
          },
          {
            path: 'update/:id',
            name: 'user-update',
            component: () =>
              import('@/views/home/homeChildren/user/UpdateUser.vue'),
          },
        ],
      },
      {
        path: 'dish',
        name: 'dish',
        redirect: '/home/dish/list',
        // component: () => import('@/views/home/homeChildren/DishView.vue'),
        children: [
          {
            path: 'list',
            name: 'dish-list',
            component: () =>
              import('@/views/home/homeChildren/dish/DishView.vue'),
          },
          {
            path: 'add',
            name: 'dish-add',
            component: () =>
              import('@/views/home/homeChildren/dish/AddDish.vue'),
          },
          {
            path: 'update/:id',
            name: 'dish-update',
            component: () =>
              import('@/views/home/homeChildren/dish/UpdateDish.vue'),
          },
        ],
      },      // 3. 管理员模块
      {
        path: 'admin',
        name: 'admin',
        redirect: '/home/admin/list',
        children: [
          {
            path: 'list',
            name: 'admin-list',
            component: () =>
              import('@/views/home/homeChildren/admin/AdminView.vue'),
          },
          {
            path: 'add',
            name: 'admin-add',
            component: () =>
              import('@/views/home/homeChildren/admin/AddAdmin.vue'),
          },
        ],
      },      // 4. 公告管理模块
      {
        path: 'notice',
        name: 'notice',
        redirect: '/home/notice/list',
        children: [
          {
            path: 'list',
            name: 'notice-list',
            component: () =>
              import('@/views/home/homeChildren/notice/NoticeView.vue'),
          },
          {
            path: 'add',
            name: 'notice-add',
            component: () =>
              import('@/views/home/homeChildren/notice/AddNotice.vue'),
          },
        ],
      },
      {      // 5. 订单管理模块
        path: 'order',
        name: 'order',
        // component: () => import('@/views/home/homeChildren/OrderView.vue'),
        redirect: '/home/order/list',
        children: [
          {
            path: 'list',
            name: 'order-list',
            component: () =>
              import('@/views/home/homeChildren/order/OrderView.vue'),
          },
          {
            path: 'update',
            name: 'order-update',
            component: () =>
              import('@/views/home/homeChildren/order/UpdateOrder.vue'),
          },
        ],
      },
      {    // 6. 口味管理
        path: 'flavor',
        name: 'flavor',
        component: () =>
          import('@/views/home/homeChildren/flavor/FlavorView.vue'),
      },
      {      // 7. 分类管理
        path: 'type',
        name: 'type',
        component: () => import('@/views/home/homeChildren/type/TypeView.vue'),
      },
    ],
  },
]
// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})
// 全局路由守卫
router.beforeEach((to, from, next) => {
  const sessionId = localStorage.getItem('sessionid')
  if (!sessionId && to.path !== '/login') {
    // 如果sessionId为空且不是访问登录页面，则跳转到登录页面
    next('/login')
  } else {
    next()
  }
})
export default router
