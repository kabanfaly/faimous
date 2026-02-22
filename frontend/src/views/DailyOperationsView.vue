<template>
  <div class="page">
    <PageHeader>
      {{ $t('dailyOperations.title') }}
      <template #subtitle>{{ $t('dailyOperations.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body">
      <div class="section-header">
        <h2 class="section-title">{{ $t('dailyOperations.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('dailyOperations.empty')"
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
          <label>{{ $t('dailyOperations.farm') }}</label>
          <select v-model="form.farm_id" class="input">
            <option value="">{{ $t('common.selectFarm') }}</option>
            <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.period') }}</label>
          <input v-model="form.period" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.collect1') }}</label>
          <input v-model.number="form.collect1" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.collect2') }}</label>
          <input v-model.number="form.collect2" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.collect3') }}</label>
          <input v-model.number="form.collect3" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.collect4') }}</label>
          <input v-model.number="form.collect4" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.broken') }}</label>
          <input v-model.number="form.broken" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.hens') }}</label>
          <input v-model.number="form.hens" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.dead') }}</label>
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
import {
  getDailyOperations,
  getDailyOperation,
  createDailyOperation,
  updateDailyOperation,
  deleteDailyOperation,
} from '../api/production'
import { getFarms } from '../api/farms'

const { t } = useI18n()
const items = ref([])
const farms = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)
const form = ref({
  date: new Date().toISOString().slice(0, 10),
  farm_id: '',
  period: '',
  collect1: null,
  collect2: null,
  collect3: null,
  collect4: null,
  broken: null,
  hens: null,
  dead: null,
})

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'period', label: t('dailyOperations.period') },
  { key: 'collect1', label: t('dailyOperations.collect1'), value: (item) => item.collect1 ?? '—' },
  { key: 'collect2', label: t('dailyOperations.collect2'), value: (item) => item.collect2 ?? '—' },
  { key: 'collect3', label: t('dailyOperations.collect3'), value: (item) => item.collect3 ?? '—' },
  { key: 'collect4', label: t('dailyOperations.collect4'), value: (item) => item.collect4 ?? '—' },
  { key: 'broken', label: t('dailyOperations.broken'), value: (item) => item.broken ?? '—' },
  { key: 'hens', label: t('dailyOperations.hens'), value: (item) => item.hens ?? '—' },
  { key: 'dead', label: t('dailyOperations.dead'), value: (item) => item.dead ?? '—' },
  {
    key: 'farm_id',
    label: t('dailyOperations.farm'),
    value: (item) => {
      const farm = farms.value.find((f) => f.id === item.farm_id)
      return farm?.name ?? '—'
    },
  },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('dailyOperations.title')}` : `${t('common.add')} ${t('dailyOperations.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.date} — ${t('dailyOperations.confirmDelete')}` : ''
)

function openAdd() {
  resetForm()
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
  resetForm()
}

function resetForm() {
  editing.value = null
  form.value = {
    date: new Date().toISOString().slice(0, 10),
    farm_id: '',
    period: '',
    collect1: null,
    collect2: null,
    collect3: null,
    collect4: null,
    broken: null,
    hens: null,
    dead: null,
  }
}

async function load() {
  loading.value = true
  try {
    const [itemsData, farmsData] = await Promise.all([getDailyOperations(), getFarms()])
    items.value = itemsData
    farms.value = farmsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function startEdit(item) {
  try {
    const op = await getDailyOperation(item.id)
    editing.value = item.id
    form.value = {
      date: op.date,
      farm_id: op.farm_id || '',
      period: op.period || '',
      collect1: op.collect1,
      collect2: op.collect2,
      collect3: op.collect3,
      collect4: op.collect4,
      broken: op.broken,
      hens: op.hens,
      dead: op.dead,
    }
    modalOpen.value = true
  } catch (e) {
    console.error(e)
  }
}

function confirmDelete(item) {
  itemToDelete.value = item
  deleteDialogOpen.value = true
}

async function doConfirmDelete() {
  if (!itemToDelete.value) return
  deleteLoading.value = true
  try {
    await deleteDailyOperation(itemToDelete.value.id)
    deleteDialogOpen.value = false
    itemToDelete.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteLoading.value = false
  }
}

async function submit() {
  try {
    const payload = {
      date: form.value.date,
      farm_id: form.value.farm_id || undefined,
      period: form.value.period || undefined,
      collect1: form.value.collect1,
      collect2: form.value.collect2,
      collect3: form.value.collect3,
      collect4: form.value.collect4,
      broken: form.value.broken,
      hens: form.value.hens,
      dead: form.value.dead,
    }
    if (editing.value) {
      await updateDailyOperation(editing.value, payload)
    } else {
      await createDailyOperation(payload)
    }
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>
