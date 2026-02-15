<template>
  <button
    type="button"
    class="icon-btn"
    :class="{ 'icon-btn--danger': danger }"
    :title="title"
    :aria-label="title"
    @click="$emit('click')"
  >
    <!-- Edit (pencil) -->
    <svg v-if="type === 'edit'" class="icon-btn__svg" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
    <!-- Delete (trash) -->
    <svg v-else-if="type === 'delete'" class="icon-btn__svg" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <line x1="10" y1="11" x2="10" y2="17" />
      <line x1="14" y1="11" x2="14" y2="17" />
    </svg>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, required: true }, // 'edit' | 'delete'
  title: { type: String, default: '' },
})

defineEmits(['click'])

const danger = computed(() => props.type === 'delete')
</script>

<style scoped>
.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  color: var(--color-text-muted);
  background: none;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: color var(--transition), background var(--transition);
}

.icon-btn:hover {
  color: var(--color-text);
  background: var(--color-background-alt);
}

.icon-btn--danger:hover {
  color: var(--color-error, #ef4444);
}

.icon-btn__svg {
  flex-shrink: 0;
}
</style>
