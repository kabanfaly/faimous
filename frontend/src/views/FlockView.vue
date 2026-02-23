<template>
  <div class="page">
    <PageHeader>
      {{ $t('production.flock') }}
      <template #subtitle>{{ $t('production.title') }}</template>
    </PageHeader>
    <section class="card card-body">
      <div class="section-header">
        <h2 class="section-title">{{ $t('production.flock') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <div v-if="totals && items.length" class="totals-row">
        <span class="totals-label">{{ $t('production.totalHens') }}:</span>
        <span class="totals-value">{{ totals.total_hens }}</span>
        <span class="totals-label">{{ $t('production.dead') }}:</span>
        <span class="totals-value">{{ totals.dead }}</span>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('production.emptyFlock')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="modalOpen" :title="modalTitle">
      <form @submit.prevent="submit" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="form.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('production.totalHens') }}</label>
          <input v-model.number="form.total_hens" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.dead') }}</label>
          <input v-model.number="form.dead" type="number" class="input" min="0" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <ConfirmDialog
      v-model="deleteDialogOpen"
      :message="deleteDialogMessage"
      :loading="deleteLoading"
      @confirm="doConfirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import PaginatedTable from '../components/PaginatedTable.vue'
import Modal from '../components/Modal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import IconButton from '../components/IconButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { getFlock, createFlock, updateFlock, deleteFlock } from '../api/production'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ date: new Date().toISOString().slice(0, 10), total_hens: 0, dead: 0 })
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('production.flock')}` : `${t('common.add')} ${t('production.flock')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.date} — ${t('production.confirmDeleteFlock')}` : ''
)

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'total_hens', label: t('production.totalHens') },
  { key: 'dead', label: t('production.dead') },
])

const totals = computed(() => {
  if (!items.value.length) return null
  return items.value.reduce(
    (acc, item) => ({
      total_hens: acc.total_hens + (item.total_hens ?? 0),
      dead: acc.dead + (item.dead ?? 0),
    }),
    { total_hens: 0, dead: 0 }
  )
})

function openAdd() {
  editing.value = null
  form.value = { date: new Date().toISOString().slice(0, 10), total_hens: 0, dead: 0 }
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
  editing.value = null
}

function startEdit(item) {
  editing.value = item.id
  form.value = {
    date: item.date,
    total_hens: item.total_hens ?? 0,
    dead: item.dead ?? 0,
  }
  modalOpen.value = true
}

function confirmDelete(item) {
  itemToDelete.value = item
  deleteDialogOpen.value = true
}

async function doConfirmDelete() {
  if (!itemToDelete.value) return
  deleteLoading.value = true
  try {
    await deleteFlock(itemToDelete.value.id)
    deleteDialogOpen.value = false
    itemToDelete.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteLoading.value = false
  }
}

async function load() {
  loading.value = true
  try {
    items.value = await getFlock()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submit() {
  try {
    if (editing.value) {
      await updateFlock(editing.value, form.value)
    } else {
      await createFlock(form.value)
    }
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

<style scoped>
.totals-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2) var(--space-4);
  padding: var(--space-3) 0;
  margin-bottom: var(--space-4);
  border-bottom: 1px solid var(--color-border, rgba(0, 0, 0, 0.08));
  font-size: var(--text-sm);
}

.totals-label {
  color: var(--color-text-muted);
}

.totals-value {
  font-weight: 600;
  color: var(--color-text);
}
</style>
