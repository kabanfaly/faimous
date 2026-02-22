<template>
  <div class="page">
    <PageHeader>
      {{ $t('productTypes.title') }}
      <template #subtitle>{{ $t('productTypes.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('productTypes.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('productTypes.empty')"
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
          <label class="required">{{ $t('productTypes.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('productTypes.farm') }}</label>
          <select v-model="form.farm_id" class="input" required>
            <option value="" disabled>{{ $t('common.selectFarm') }}</option>
            <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
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
import { getProductTypes, createProductType, updateProductType, deleteProductType } from '../api/productTypes'
import { getFarms } from '../api/farms'

const { t } = useI18n()
const items = ref([])
const farms = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', farm_id: '' })
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const columns = computed(() => [
  { key: 'name', label: t('productTypes.name') },
  {
    key: 'farm',
    label: t('productTypes.farm'),
    value: (item) => item.farm?.name ?? '—',
  },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('productTypes.title')}` : `${t('common.add')} ${t('productTypes.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.name} — ${t('productTypes.confirmDelete')}` : ''
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
  form.value = { name: '', farm_id: '' }
}

async function load() {
  loading.value = true
  try {
    const [itemsData, farmsData] = await Promise.all([getProductTypes(), getFarms()])
    items.value = itemsData
    farms.value = farmsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { name: item.name, farm_id: item.farm_id || '' }
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
    await deleteProductType(itemToDelete.value.id)
    deleteDialogOpen.value = false
    itemToDelete.value = null
    await load()
  } catch (e) {
    if (e.response?.status === 409 && e.response?.data?.message) {
      window.alert(e.response.data.message)
    } else {
      console.error(e)
    }
  } finally {
    deleteLoading.value = false
  }
}

async function submit() {
  try {
    if (editing.value) await updateProductType(editing.value, form.value)
    else await createProductType(form.value)
    closeModal()
    await load()
  } catch (e) {
    if (e.response?.status === 409 && e.response?.data?.message) {
      window.alert(e.response.data.message)
    } else {
      console.error(e)
    }
  }
}

onMounted(load)
</script>
