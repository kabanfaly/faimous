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
          <label class="required">{{ $t('products.type') }}</label>
          <select v-model="form.product_type_id" class="input" required>
            <option value="" disabled>{{ $t('common.selectProduct') }}</option>
            <option v-for="pt in productTypes" :key="pt.id" :value="pt.id">{{ pt.name }}</option>
          </select>
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
import { getProducts, createProduct, updateProduct, deleteProduct } from '../api/products'
import { getProductTypes } from '../api/productTypes'

const { t } = useI18n()
const items = ref([])
const productTypes = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', description: '', product_type_id: '', unit: '' })
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const columns = computed(() => [
  { key: 'name', label: t('products.name') },
  { key: 'description', label: t('products.description') },
  {
    key: 'product_type',
    label: t('products.type'),
    value: (item) => item.product_type?.name ?? '—',
  },
  { key: 'unit', label: t('products.unit') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('products.title')}` : `${t('common.add')} ${t('products.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.name} — ${t('products.confirmDelete')}` : ''
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
  form.value = { name: '', description: '', product_type_id: '', unit: '' }
}

async function load() {
  loading.value = true
  try {
    const [itemsData, typesData] = await Promise.all([getProducts(), getProductTypes()])
    items.value = itemsData
    productTypes.value = typesData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = {
    name: item.name,
    description: item.description || '',
    product_type_id: item.product_type_id || '',
    unit: item.unit || '',
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
    await deleteProduct(itemToDelete.value.id)
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
      ...form.value,
      product_type_id: form.value.product_type_id || undefined,
    }
    if (editing.value) await updateProduct(editing.value, payload)
    else await createProduct(payload)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

