<template>
  <div class="main-layout" :class="{ 'sidebar-open': sidebarOpen }">
    <div class="sidebar-overlay" aria-hidden="true" @click="sidebarOpen = false" />
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="sidebar-logo">Faimous</span>
        <button type="button" class="sidebar-close-btn" aria-label="Close menu" @click="sidebarOpen = false">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
      <nav class="sidebar-nav" @click="onNavClick">
        <template v-for="(group, gKey) in navGroups" :key="gKey">
          <div class="nav-group">
            <span class="nav-group-label">{{ $t(`nav.${group.labelKey}`) }}</span>
            <template v-for="item in group.items" :key="item.to || item.i18nKey">
              <template v-if="item.children">
                <span class="nav-submenu-label">{{ $t(`nav.${item.i18nKey}`) }}</span>
                <router-link
                  v-for="child in item.children"
                  :key="child.to"
                  :to="child.to"
                  class="nav-link nav-link--sub"
                  active-class="nav-link-active"
                  exact-active-class="nav-link-active"
                >
                  <NavIcon :name="child.icon" />
                  <span>{{ $t(`nav.${child.i18nKey}`) }}</span>
                </router-link>
              </template>
              <router-link
                v-else
                :to="item.to"
                class="nav-link"
                exact-active-class="nav-link-active"
              >
                <NavIcon :name="item.icon" />
                <span>{{ $t(`nav.${item.i18nKey}`) }}</span>
              </router-link>
            </template>
          </div>
        </template>
      </nav>
      <div class="sidebar-footer">
        <button type="button" class="btn btn-ghost logout-btn" @click="handleLogout">
          {{ $t('auth.logout') }}
        </button>
      </div>
    </aside>
    <div class="main-area">
      <header class="header-bar">
        <button type="button" class="header-menu-btn" aria-label="Open menu" @click="sidebarOpen = !sidebarOpen">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <div class="header-actions">
          <div class="header-locale">
            <button type="button" class="header-locale-btn" :class="{ active: locale === 'fr' }" @click="setLocale('fr')">FR</button>
            <span class="header-locale-sep">/</span>
            <button type="button" class="header-locale-btn" :class="{ active: locale === 'en' }" @click="setLocale('en')">EN</button>
          </div>
          <div ref="userMenuRef" class="header-user-menu" :class="{ open: userMenuOpen }">
            <button type="button" class="header-user-trigger" aria-haspopup="true" :aria-expanded="userMenuOpen" @click="userMenuOpen = !userMenuOpen">
              <span class="header-user-avatar">{{ userInitials }}</span>
              <span class="header-user-name">{{ userDisplayName }}</span>
              <svg class="header-user-chevron" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <Transition name="dropdown">
              <div v-show="userMenuOpen" class="header-user-dropdown" role="menu">
                <router-link to="/account" class="header-dropdown-item" role="menuitem" @click="userMenuOpen = false">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  <span>{{ $t('header.account') }}</span>
                </router-link>
                <router-link to="/settings" class="header-dropdown-item" role="menuitem" @click="userMenuOpen = false">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                  <span>{{ $t('header.settings') }}</span>
                </router-link>
                <div class="header-dropdown-divider" role="separator" />
                <button type="button" class="header-dropdown-item header-dropdown-item--danger" role="menuitem" @click="handleLogout">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                  <span>{{ $t('auth.logout') }}</span>
                </button>
              </div>
            </Transition>
          </div>
        </div>
      </header>
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../store/auth'
import NavIcon from '../components/NavIcon.vue'

const router = useRouter()
const { locale } = useI18n()
const auth = useAuthStore()
const userMenuRef = ref(null)
const userMenuOpen = ref(false)
const sidebarOpen = ref(true)

function onNavClick() {
  if (typeof window !== 'undefined' && window.innerWidth < 769) {
    sidebarOpen.value = false
  }
}

const userDisplayName = computed(() => {
  const u = auth.user
  const o = auth.organisation
  if (u?.first_name || u?.last_name) {
    return [u.first_name, u.last_name].filter(Boolean).join(' ').trim()
  }
  if (u?.email) return u.email
  if (o?.name) return o.name
  return 'Account'
})

const userInitials = computed(() => {
  const u = auth.user
  const o = auth.organisation
  if (u?.first_name || u?.last_name) {
    const first = (u.first_name || '').charAt(0)
    const last = (u.last_name || '').charAt(0)
    return (first + last).toUpperCase() || '?'
  }
  if (o?.name) return o.name.slice(0, 2).toUpperCase()
  if (u?.email) {
    const part = u.email.split('@')[0]
    return part.slice(0, 2).toUpperCase()
  }
  return '?'
})

function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}

function handleLogout() {
  userMenuOpen.value = false
  auth.logout()
  router.push('/auth/login')
}

function onDocumentClick(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    userMenuOpen.value = false
  }
}

const MOBILE_BREAKPOINT = 769

function closeSidebarIfMobile() {
  if (typeof window !== 'undefined' && window.innerWidth < MOBILE_BREAKPOINT) {
    sidebarOpen.value = false
  }
}

onMounted(() => {
  if (auth.token && !auth.user && !auth.organisation) {
    auth.fetchMe().catch(() => {})
  }
  closeSidebarIfMobile()
  window.addEventListener('resize', closeSidebarIfMobile)
  document.addEventListener('click', onDocumentClick)
})

onUnmounted(() => {
  window.removeEventListener('resize', closeSidebarIfMobile)
  document.removeEventListener('click', onDocumentClick)
})

const navGroups = [
  {
    labelKey: 'groupOverview',
    items: [{ to: '/', i18nKey: 'dashboard', icon: 'dashboard' }],
  },
  {
    labelKey: 'groupFarm',
    items: [
      { to: '/production', i18nKey: 'production', icon: 'production', children: [
        { to: '/production', i18nKey: 'productionOverview', icon: 'production' },
        { to: '/production/eggs', i18nKey: 'productionEggs', icon: 'production' },
        { to: '/production/flock', i18nKey: 'productionFlock', icon: 'flock' },
      ]},
      { to: '/daily-operations', i18nKey: 'dailyOperations', icon: 'dailyOperations' },
      { to: '/feed', i18nKey: 'feed', icon: 'feed' },
      { to: '/stock', i18nKey: 'stock', icon: 'stock', children: [
        { to: '/stock', i18nKey: 'stockProducts', icon: 'stock' },
        { to: '/stock/movements', i18nKey: 'stockMovements', icon: 'stockMovements' },
      ]},
    ],
  },
  {
    labelKey: 'groupCommerce',
    items: [
      { to: '/sales', i18nKey: 'sales', icon: 'sales' },
      { to: '/purchases', i18nKey: 'purchases', icon: 'purchases' },
      { to: '/expenses', i18nKey: 'expenses', icon: 'expenses' },
      { to: '/financing', i18nKey: 'financing', icon: 'financing' },
    ],
  },
  {
    labelKey: 'groupDirectory',
    items: [
      { to: '/suppliers', i18nKey: 'suppliers', icon: 'suppliers' },
      { to: '/wholesalers', i18nKey: 'wholesalers', icon: 'wholesalers' },
      { to: '/cities', i18nKey: 'cities', icon: 'cities' },
      { to: '/shareholders', i18nKey: 'shareholders', icon: 'shareholders' },
      { to: '/farms', i18nKey: 'farms', icon: 'farms' },
    ],
  },
  {
    labelKey: 'groupSetup',
    items: [
      { to: '/users', i18nKey: 'users', icon: 'users' },
      { to: '/product-types', i18nKey: 'productTypes', icon: 'productTypes' },
      { to: '/expense-categories', i18nKey: 'expenseCategories', icon: 'expenseCategories' },
    ],
  },
]
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background: var(--color-sidebar);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 150;
  transition: opacity 0.2s ease;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-6);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-logo {
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--color-primary);
  letter-spacing: -0.02em;
}

.sidebar-close-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  color: var(--color-sidebar-text);
  background: none;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: color var(--transition), background var(--transition);
}

.sidebar-close-btn:hover {
  color: var(--color-sidebar-text-active);
  background: var(--color-sidebar-hover);
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  overflow-y: auto;
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.nav-group-label {
  font-size: 0.65rem;
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-sidebar-text);
  opacity: 0.65;
  padding: var(--space-2) var(--space-4) var(--space-1);
  margin-top: var(--space-2);
}

.nav-group:first-child .nav-group-label {
  margin-top: 0;
}

.nav-submenu-label {
  font-size: 0.7rem;
  font-weight: var(--font-semibold);
  color: var(--color-sidebar-text);
  opacity: 0.7;
  padding: var(--space-2) var(--space-4) var(--space-1);
  margin-top: var(--space-1);
  display: block;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-sidebar-text);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: color var(--transition), background var(--transition);
}

.nav-link:hover {
  color: var(--color-sidebar-text-active);
  background: var(--color-sidebar-hover);
}

.nav-link-active {
  color: var(--color-sidebar-text-active);
  background: var(--color-sidebar-active);
}

.nav-link-active:hover {
  background: var(--color-sidebar-active);
  opacity: 0.95;
}

.nav-link--sub {
  padding-left: var(--space-8);
}

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.logout-btn {
  width: 100%;
  justify-content: center;
  color: var(--color-sidebar-text);
}

.logout-btn:hover {
  color: var(--color-sidebar-text-active);
  background: var(--color-sidebar-hover);
}

.main-area {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: var(--color-background);
}

.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-6);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.header-menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  margin-right: var(--space-2);
  margin-left: calc(-1 * var(--space-2));
  color: var(--color-text-muted);
  background: none;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: color var(--transition), background var(--transition);
}

.header-menu-btn:hover {
  color: var(--color-text);
  background: var(--color-background-alt);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.header-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--color-text-muted);
  border-radius: var(--radius-md);
  transition: color var(--transition), background var(--transition);
}

.header-icon-btn:hover {
  color: var(--color-text);
  background: var(--color-background-alt);
}

.header-locale {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.header-locale-btn {
  padding: var(--space-1) var(--space-2);
  color: var(--color-text-muted);
  background: none;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: color var(--transition), background var(--transition);
}

.header-locale-btn:hover {
  color: var(--color-text);
}

.header-locale-btn.active {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.header-locale-sep {
  color: var(--color-text-muted);
  opacity: 0.6;
  user-select: none;
}

.header-user-menu {
  position: relative;
}

.header-user-trigger {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text);
  background: var(--color-background-alt);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}

.header-user-trigger:hover {
  background: var(--color-background);
  border-color: var(--color-text-muted);
}

.header-user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  font-size: 0.7rem;
  font-weight: var(--font-semibold);
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.header-user-name {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-user-chevron {
  flex-shrink: 0;
  opacity: 0.7;
  transition: transform var(--transition);
}

.header-user-menu.open .header-user-chevron {
  transform: rotate(180deg);
}

.header-user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  min-width: 200px;
  padding: var(--space-2);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  z-index: 100;
}

.header-dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text);
  text-decoration: none;
  text-align: left;
  background: none;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--transition);
}

.header-dropdown-item:hover {
  background: var(--color-background-alt);
}

.header-dropdown-item--danger:hover {
  color: var(--color-error);
  background: var(--color-error-bg);
}

.header-dropdown-item svg {
  flex-shrink: 0;
  opacity: 0.8;
}

.header-dropdown-divider {
  height: 1px;
  margin: var(--space-2) 0;
  background: var(--color-border);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.12s ease, transform 0.12s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.main-content {
  flex: 1;
  min-width: 0;
  padding: var(--space-8);
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Desktop: fixed sidebar, can be collapsed */
@media (min-width: 769px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 260px;
    height: 100vh;
    z-index: 100;
    transition: width 0.2s ease, transform 0.2s ease;
  }

  .main-layout:not(.sidebar-open) .sidebar {
    width: 0;
    min-width: 0;
    overflow: hidden;
    border-right-width: 0;
  }

  .main-area {
    margin-left: 260px;
    transition: margin-left 0.2s ease;
  }

  .main-layout:not(.sidebar-open) .main-area {
    margin-left: 0;
  }
}

/* Mobile: overlay sidebar */
@media (max-width: 768px) {
  .sidebar-overlay {
    display: block;
    opacity: 0;
    pointer-events: none;
  }

  .main-layout.sidebar-open .sidebar-overlay {
    opacity: 1;
    pointer-events: auto;
  }

  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 200;
    width: 280px;
    max-width: 85vw;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    box-shadow: none;
  }

  .main-layout.sidebar-open .sidebar {
    transform: translateX(0);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
  }

  .sidebar-close-btn {
    display: flex;
  }

  .header-bar {
    padding-left: var(--space-4);
  }

  .header-user-name {
    max-width: 100px;
  }

  .main-content {
    padding: var(--space-4);
  }
}
</style>
