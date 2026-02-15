<template>
  <div class="page">
    <PageHeader>
      {{ $t('farms.title') }}
      <template #subtitle>{{ $t('farms.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('farms.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('farms.empty')"
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
          <label class="required">{{ $t('farms.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('farms.location') }}</label>
          <input v-model="form.location" type="text" class="input" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeModal">{{ $t('common.cancel') }}</button>
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
import { getFarms, createFarm, updateFarm, deleteFarm } from '../api/farms'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', location: '' })

const columns = computed(() => [
  { key: 'name', label: t('farms.name') },
  { key: 'location', label: t('farms.location') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('farms.title')}` : `${t('common.add')} ${t('farms.title')}`
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
  form.value = { name: '', location: '' }
}

async function load() {
  loading.value = true
  try {
    items.value = await getFarms()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { name: item.name, location: item.location || '' }
  modalOpen.value = true
}

function confirmDelete(item) {
  if (window.confirm(`${item.name} — ${t('farms.confirmDelete')}`)) doDelete(item.id)
}

async function doDelete(id) {
  try {
    await deleteFarm(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submit() {
  try {
    if (editing.value) await updateFarm(editing.value, form.value)
    else await createFarm(form.value)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

