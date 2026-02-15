<template>
  <header class="page-header">
    <h1 class="page-title">
      <NavIcon v-if="icon" :name="icon" class="page-title__icon" />
      <span class="page-title__text"><slot /></span>
    </h1>
    <p v-if="$slots.subtitle" class="page-subtitle"><slot name="subtitle" /></p>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavIcon from './NavIcon.vue'

const route = useRoute()
const icon = computed(() => route.meta?.icon ?? null)
</script>

<style scoped>
.page-header {
  margin-bottom: var(--space-8);
}

.page-title {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin: 0;
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-text);
  line-height: 1.2;
}

.page-title__icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  opacity: 0.9;
}

.page-title__icon :deep(.nav-icon),
.page-title__icon :deep(.nav-icon__svg) {
  width: 100%;
  height: 100%;
}

.page-title__text {
  min-width: 0;
}

.page-subtitle {
  margin: var(--space-1) 0 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  line-height: 1.4;
}
</style>
