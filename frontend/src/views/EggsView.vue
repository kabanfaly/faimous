<template>
  <div class="page">
    <PageHeader>
      {{ $t('production.eggs') }}
      <template #subtitle>{{ $t('production.title') }}</template>
    </PageHeader>
    <section class="card card-body">
      <div class="section-header">
        <h2 class="section-title">{{ $t('production.eggs') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <div v-if="totals && items.length" class="totals-row">
        <span class="totals-label">{{ $t('production.eggsCount') }}:</span>
        <span class="totals-value">{{ totals.eggs_count }}</span>
        <span class="totals-label">{{ $t('production.brokenCount') }}:</span>
        <span class="totals-value">{{ totals.broken_count }}</span>
        <span class="totals-label">{{ $t('production.trays') }}:</span>
        <span class="totals-value">{{ totals.trays }}</span>
        <span class="totals-label">{{ $t('production.remaining') }}:</span>
        <span class="totals-value">{{ totals.remaining }}</span>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('production.emptyEggs')"
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
          <label>{{ $t('production.eggsCount') }}</label>
          <input v-model.number="form.eggs_count" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.brokenCount') }}</label>
          <input v-model.number="form.broken_count" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.trays') }}</label>
          <input v-model.number="form.trays" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.remaining') }}</label>
          <input v-model.number="form.remaining" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.note') }}</label>
          <textarea v-model="form.note" class="input" rows="3" />
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
import { getEggs, createEggs, updateEggs, deleteEggs } from '../api/production'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ date: new Date().toISOString().slice(0, 10), eggs_count: 0, broken_count: 0, trays: null, remaining: null, note: null })
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('production.eggs')}` : `${t('common.add')} ${t('production.eggs')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.date} — ${t('production.confirmDeleteEggs')}` : ''
)

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'eggs_count', label: t('production.eggsCount') },
  { key: 'broken_count', label: t('production.brokenCount') },
  { key: 'trays', label: t('production.trays') },
  { key: 'remaining', label: t('production.remaining') },
  { key: 'note', label: t('production.note') },
])

const totals = computed(() => {
  if (!items.value.length) return null
  return items.value.reduce(
    (acc, item) => ({
      eggs_count: acc.eggs_count + (item.eggs_count ?? 0),
      broken_count: acc.broken_count + (item.broken_count ?? 0),
      trays: acc.trays + (item.trays ?? 0),
      remaining: acc.remaining + (item.remaining ?? 0),
    }),
    { eggs_count: 0, broken_count: 0, trays: 0, remaining: 0 }
  )
})

function openAdd() {
  editing.value = null
  form.value = { date: new Date().toISOString().slice(0, 10), eggs_count: 0, broken_count: 0, trays: null, remaining: null, note: null }
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
    eggs_count: item.eggs_count ?? 0,
    broken_count: item.broken_count ?? 0,
    trays: item.trays ?? null,
    remaining: item.remaining ?? null,
    note: item.note ?? null,
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
    await deleteEggs(itemToDelete.value.id)
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
    items.value = await getEggs()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submit() {
  try {
    if (editing.value) {
      await updateEggs(editing.value, form.value)
    } else {
      await createEggs(form.value)
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
