<template>
  <div class="page">
    <PageHeader>
      {{ $t('wholesalers.title') }}
      <template #subtitle>{{ $t('wholesalers.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('wholesalers.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('wholesalers.empty')"
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
          <label class="required">{{ $t('wholesalers.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('wholesalers.city') }}</label>
          <select v-model="form.city_id" class="input">
            <option value="">{{ $t('common.selectCity') }}</option>
            <option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
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
import { getWholesalers, createWholesaler, updateWholesaler, deleteWholesaler } from '../api/wholesalers'
import { getCities } from '../api/cities'

const { t } = useI18n()
const items = ref([])
const cities = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', city_id: '' })
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const columns = computed(() => [
  { key: 'name', label: t('wholesalers.name') },
  {
    key: 'city_id',
    label: t('wholesalers.city'),
    value: (item) => {
      const city = cities.value.find((c) => c.id === item.city_id)
      return city?.name ?? '—'
    },
  },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('wholesalers.title')}` : `${t('common.add')} ${t('wholesalers.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.name} — ${t('wholesalers.confirmDelete')}` : ''
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
  form.value = { name: '', city_id: '' }
}

async function load() {
  loading.value = true
  try {
    const [itemsData, citiesData] = await Promise.all([getWholesalers(), getCities()])
    items.value = itemsData
    cities.value = citiesData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { name: item.name, city_id: item.city_id || '' }
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
    await deleteWholesaler(itemToDelete.value.id)
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
    if (editing.value) await updateWholesaler(editing.value, form.value)
    else await createWholesaler(form.value)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

