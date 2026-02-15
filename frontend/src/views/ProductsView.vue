<template>
  <div class="page">
    <PageHeader>
      {{ $t('products.title') }}
      <template #subtitle>{{ $t('products.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('products.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('products.empty')"
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
          <label class="required">{{ $t('products.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('products.description') }}</label>
          <input v-model="form.description" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('products.type') }}</label>
          <input v-model="form.type" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('products.unit') }}</label>
          <input v-model="form.unit" type="text" class="input" />
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
import { getProducts, createProduct, updateProduct, deleteProduct } from '../api/products'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', description: '', type: '', unit: '' })

const columns = computed(() => [
  { key: 'name', label: t('products.name') },
  { key: 'description', label: t('products.description') },
  { key: 'type', label: t('products.type') },
  { key: 'unit', label: t('products.unit') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('products.title')}` : `${t('common.add')} ${t('products.title')}`
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
  form.value = { name: '', description: '', type: '', unit: '' }
}

async function load() {
  loading.value = true
  try {
    items.value = await getProducts()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { name: item.name, description: item.description || '', type: item.type || '', unit: item.unit || '' }
  modalOpen.value = true
}

function confirmDelete(item) {
  if (window.confirm(`${item.name} — ${t('products.confirmDelete')}`)) doDelete(item.id)
}

async function doDelete(id) {
  try {
    await deleteProduct(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submit() {
  try {
    if (editing.value) await updateProduct(editing.value, form.value)
    else await createProduct(form.value)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

