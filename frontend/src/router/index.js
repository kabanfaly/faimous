import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/auth',
    component: () => import('../layouts/AuthLayout.vue'),
    children: [
      { path: 'login', name: 'Login', component: () => import('../views/LoginView.vue') },
      { path: 'register', name: 'Register', component: () => import('../views/RegisterView.vue') },
    ],
  },
  { path: '/login', redirect: '/auth/login' },
  { path: '/register', redirect: '/auth/register' },
  { path: '/products', redirect: '/stock' },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { icon: 'dashboard' } },
      { path: 'production', name: 'Production', component: () => import('../views/ProductionView.vue'), meta: { icon: 'production' } },
      { path: 'production/eggs', name: 'ProductionEggs', component: () => import('../views/EggsView.vue'), meta: { icon: 'production' } },
      { path: 'production/flock', name: 'ProductionFlock', component: () => import('../views/FlockView.vue'), meta: { icon: 'flock' } },
      { path: 'daily-operations', name: 'DailyOperations', component: () => import('../views/DailyOperationsView.vue'), meta: { icon: 'dailyOperations' } },
      { path: 'sales', name: 'Sales', component: () => import('../views/SalesView.vue'), meta: { icon: 'sales' } },
      { path: 'purchases', name: 'Purchases', component: () => import('../views/PurchasesView.vue'), meta: { icon: 'purchases' } },
      { path: 'stock', name: 'Stock', component: () => import('../views/StockView.vue'), meta: { icon: 'stock' } },
      { path: 'stock/movements', name: 'StockMovements', component: () => import('../views/StockMovementsView.vue'), meta: { icon: 'stockMovements' } },
      { path: 'expenses', name: 'Expenses', component: () => import('../views/ExpensesView.vue'), meta: { icon: 'expenses' } },
      { path: 'feed', name: 'Feed', component: () => import('../views/FeedView.vue'), meta: { icon: 'feed' } },
      { path: 'financing', name: 'Financing', component: () => import('../views/FinancingView.vue'), meta: { icon: 'financing' } },
      { path: 'users', name: 'Users', component: () => import('../views/UsersView.vue'), meta: { icon: 'users' } },
      { path: 'suppliers', name: 'Suppliers', component: () => import('../views/SuppliersView.vue'), meta: { icon: 'suppliers' } },
      { path: 'cities', name: 'Cities', component: () => import('../views/CitiesView.vue'), meta: { icon: 'cities' } },
      { path: 'wholesalers', name: 'Wholesalers', component: () => import('../views/WholesalersView.vue'), meta: { icon: 'wholesalers' } },
      { path: 'product-types', name: 'ProductTypes', component: () => import('../views/ProductTypesView.vue'), meta: { icon: 'productTypes' } },
      { path: 'expense-categories', name: 'ExpenseCategories', component: () => import('../views/ExpenseCategoriesView.vue'), meta: { icon: 'expenseCategories' } },
      { path: 'shareholders', name: 'Shareholders', component: () => import('../views/ShareholdersView.vue'), meta: { icon: 'shareholders' } },
      { path: 'farms', name: 'Farms', component: () => import('../views/FarmsView.vue'), meta: { icon: 'farms' } },
      { path: 'account', name: 'Account', component: () => import('../views/AccountView.vue'), meta: { icon: 'users' } },
      { path: 'settings', name: 'Settings', component: () => import('../views/SettingsView.vue'), meta: { icon: 'users' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next({ path: '/auth/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
