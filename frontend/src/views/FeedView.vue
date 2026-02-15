<template>
  <div class="page">
    <PageHeader>
      {{ $t('feed.title') }}
      <template #subtitle>{{ $t('feed.preparations') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('feed.preparations') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddPreparation">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="preparations"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('feed.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="preparationModalOpen" :title="preparationModalTitle">
      <form @submit.prevent="submitPreparation" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="form.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('feed.quantityKg') }}</label>
          <input v-model.number="form.quantity_kg" type="number" class="input" step="0.01" required />
        </div>
        <div class="form-group">
          <label>{{ $t('feed.ratio') }}</label>
          <input v-model="form.ratio" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('feed.hens') }}</label>
          <input v-model.number="form.hens_available" type="number" class="input" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closePreparationModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import PaginatedTable from '../components/PaginatedTable.vue'
import Modal from '../components/Modal.vue'
import IconButton from '../components/IconButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { getPreparations, createPreparation, updatePreparation, deletePreparation } from '../api/feed'

const { t } = useI18n()
const preparations = ref([])
const loading = ref(false)
const preparationModalOpen = ref(false)
const editingPreparation = ref(null)

const preparationModalTitle = computed(() =>
  editingPreparation.value ? `${t('common.edit')} ${t('feed.preparations')}` : `${t('common.add')} ${t('feed.preparations')}`
)

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'quantity_kg', label: t('feed.quantityKg') },
  { key: 'ratio', label: t('feed.ratio') },
  { key: 'hens_available', label: t('feed.hens') },
])
const form = ref({
  date: new Date().toISOString().slice(0, 10),
  quantity_kg: 0,
  ratio: '',
  hens_available: null,
})

function openAddPreparation() {
  editingPreparation.value = null
  form.value = { date: new Date().toISOString().slice(0, 10), quantity_kg: 0, ratio: '', hens_available: null }
  preparationModalOpen.value = true
}

function closePreparationModal() {
  preparationModalOpen.value = false
  editingPreparation.value = null
}

function startEdit(item) {
  editingPreparation.value = item.id
  form.value = {
    date: item.date,
    quantity_kg: item.quantity_kg ?? 0,
    ratio: item.ratio || '',
    hens_available: item.hens_available ?? null,
  }
  preparationModalOpen.value = true
}

function confirmDelete(item) {
  if (window.confirm(`${item.date} — ${t('feed.confirmDelete')}`)) doDeletePreparation(item.id)
}

async function doDeletePreparation(id) {
  try {
    await deletePreparation(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function load() {
  loading.value = true
  try {
    preparations.value = await getPreparations()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitPreparation() {
  try {
    if (editingPreparation.value) {
      await updatePreparation(editingPreparation.value, form.value)
    } else {
      await createPreparation(form.value)
    }
    closePreparationModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

