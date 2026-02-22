<template>
  <div class="page">
    <PageHeader>
      {{ $t('cities.title') }}
      <template #subtitle>{{ $t('cities.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('cities.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('cities.empty')"
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
          <label class="required">{{ $t('cities.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('cities.prefecture') }}</label>
          <input v-model="form.prefecture" type="text" class="input" />
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
import { getCities, createCity, updateCity, deleteCity } from '../api/cities'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', prefecture: '' })
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const columns = computed(() => [
  { key: 'name', label: t('cities.name') },
  { key: 'prefecture', label: t('cities.prefecture') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('cities.title')}` : `${t('common.add')} ${t('cities.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.name} — ${t('cities.confirmDelete')}` : ''
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
  form.value = { name: '', prefecture: '' }
}

async function load() {
  loading.value = true
  try {
    items.value = await getCities()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { name: item.name, prefecture: item.prefecture || '' }
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
    await deleteCity(itemToDelete.value.id)
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
    if (editing.value) await updateCity(editing.value, form.value)
    else await createCity(form.value)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

