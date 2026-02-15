<template>
  <div class="paginated-table">
    <div class="table-wrapper">
      <table class="entity-table" v-if="paginatedItems.length">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key || col.label">{{ col.label }}</th>
            <th v-if="hasActionsSlot" class="th-actions">{{ $t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedItems" :key="item.id">
            <td v-for="col in columns" :key="col.key || col.label">
              {{ getCellValue(item, col) }}
            </td>
            <td v-if="hasActionsSlot" class="td-actions">
              <slot name="actions" :item="item" />
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!loading" class="text-muted table-empty">{{ emptyText }}</p>
      <p v-else class="text-muted table-loading">{{ $t('common.loading') }}</p>
    </div>
    <div v-if="totalPages > 1" class="pagination">
      <span class="pagination-info">
        {{ $t('pagination.showing', { from: startIndex + 1, to: Math.min(endIndex, items.length), total: items.length }) }}
      </span>
      <div class="pagination-controls">
        <button
          type="button"
          class="btn btn-ghost btn-sm"
          :disabled="currentPage <= 1"
          @click="currentPage--"
        >
          {{ $t('pagination.prev') }}
        </button>
        <span class="pagination-page">{{ $t('pagination.pageOf', { page: currentPage, total: totalPages }) }}</span>
        <button
          type="button"
          class="btn btn-ghost btn-sm"
          :disabled="currentPage >= totalPages"
          @click="currentPage++"
        >
          {{ $t('pagination.next') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  columns: { type: Array, required: true },
  perPage: { type: Number, default: 10 },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: '' },
})

const slots = defineSlots()

const hasActionsSlot = computed(() => !!slots.actions)

const currentPage = ref(1)

const totalPages = computed(() =>
  props.items.length ? Math.ceil(props.items.length / props.perPage) : 1
)

const startIndex = computed(() => (currentPage.value - 1) * props.perPage)
const endIndex = computed(() => startIndex.value + props.perPage)

const paginatedItems = computed(() =>
  props.items.slice(startIndex.value, endIndex.value)
)

function getCellValue(item, col) {
  if (col.value && typeof col.value === 'function') return col.value(item)
  const val = col.key ? item[col.key] : ''
  return val != null ? val : '—'
}

watch(() => props.items, () => { currentPage.value = 1 }, { immediate: true })
</script>

<style scoped>
.paginated-table { width: 100%; }
.table-wrapper { overflow-x: auto; border-radius: var(--radius-md); border: 1px solid var(--color-border); }
.entity-table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); }
.entity-table th,
.entity-table td { padding: var(--space-3) var(--space-4); text-align: left; border-bottom: 1px solid var(--color-border); }
.entity-table th { background: var(--color-background-alt); font-weight: var(--font-semibold); color: var(--color-text); }
.entity-table tbody tr:hover { background: var(--color-background-alt); }
.entity-table tbody tr:last-child td { border-bottom: none; }
.th-actions, .td-actions { width: 1%; white-space: nowrap; text-align: right; }
.td-actions { display: flex; gap: var(--space-2); justify-content: flex-end; }
.table-empty, .table-loading { padding: var(--space-6); text-align: center; margin: 0; }
.pagination { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-3); margin-top: var(--space-4); padding-top: var(--space-4); border-top: 1px solid var(--color-border); font-size: var(--text-sm); color: var(--color-text-muted); }
.pagination-controls { display: flex; align-items: center; gap: var(--space-3); }
.btn-sm { padding: var(--space-2) var(--space-3); font-size: var(--text-xs); }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
