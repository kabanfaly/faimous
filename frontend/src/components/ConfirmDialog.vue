<template>
  <Teleport to="body">
    <Transition name="confirm">
      <div
        v-if="modelValue"
        class="confirm-overlay"
        role="alertdialog"
        aria-modal="true"
        :aria-labelledby="titleId"
        :aria-describedby="descId"
        @click.self="cancel"
      >
        <div class="confirm-dialog" @keydown.esc="cancel">
          <div class="confirm-dialog__icon" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
          </div>
          <h2 :id="titleId" class="confirm-dialog__title">{{ title || $t('common.confirmDeleteTitle') }}</h2>
          <p :id="descId" class="confirm-dialog__message">{{ message }}</p>
          <div class="confirm-dialog__actions">
            <button
              type="button"
              class="btn btn-ghost"
              :disabled="loading"
              @click="cancel"
            >
              {{ $t('common.cancel') }}
            </button>
            <button
              type="button"
              class="btn confirm-dialog__delete"
              :disabled="loading"
              @click="confirm"
            >
              {{ loading ? $t('common.loading') : $t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: '' },
  message: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const titleId = computed(() => `confirm-title-${Math.random().toString(36).slice(2)}`)
const descId = computed(() => `confirm-desc-${Math.random().toString(36).slice(2)}`)

function confirm() {
  if (props.loading) return
  emit('confirm')
}

function cancel() {
  if (props.loading) return
  emit('update:modelValue', false)
  emit('cancel')
}
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.confirm-dialog {
  width: 100%;
  max-width: 400px;
  padding: var(--space-8);
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
  text-align: center;
}

.confirm-dialog__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-5);
  color: var(--color-error);
  background: var(--color-error-bg);
  border-radius: 50%;
}

.confirm-dialog__title {
  margin: 0 0 var(--space-2);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
}

.confirm-dialog__message {
  margin: 0 0 var(--space-6);
  font-size: var(--text-base);
  line-height: 1.5;
  color: var(--color-text-muted);
}

.confirm-dialog__actions {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
  flex-wrap: wrap;
}

.confirm-dialog__delete {
  color: white;
  background: var(--color-error);
}

.confirm-dialog__delete:hover:not(:disabled) {
  background: #b91c1c;
  color: white;
}

.confirm-dialog__delete:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.confirm-enter-active,
.confirm-leave-active {
  transition: opacity 0.2s ease;
}

.confirm-enter-active .confirm-dialog,
.confirm-leave-active .confirm-dialog {
  transition: transform 0.2s ease;
}

.confirm-enter-from,
.confirm-leave-to {
  opacity: 0;
}

.confirm-enter-from .confirm-dialog,
.confirm-leave-to .confirm-dialog {
  transform: scale(0.96);
}
</style>
